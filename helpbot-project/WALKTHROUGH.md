# HelpBot — Detailed Project Walkthrough

This guide walks through every part of the project from first principles — what each concept is, why it exists, how the code implements it, and what actually happens at runtime. Read `README.md` for setup instructions and the command reference. This guide is about understanding.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Startup Sequence](#2-startup-sequence)
3. [Settings and Configuration](#3-settings-and-configuration)
4. [The System Prompt](#4-the-system-prompt)
5. [Prompt Caching](#5-prompt-caching)
6. [Conversation History](#6-conversation-history)
7. [A Full Chat Turn — Step by Step](#7-a-full-chat-turn--step-by-step)
8. [Tool Use — How Claude Calls Functions](#8-tool-use--how-claude-calls-functions)
9. [Streaming Responses](#9-streaming-responses)
10. [RAG — Retrieval-Augmented Generation](#10-rag--retrieval-augmented-generation)
11. [Structured Output — The Return Request Form](#11-structured-output--the-return-request-form)
12. [Response Prefilling](#12-response-prefilling)
13. [Image Input](#13-image-input)
14. [Temperature Control](#14-temperature-control)
15. [Full Conversation Trace](#15-full-conversation-trace)

---

## 1. Project Overview

HelpBot is a customer support chatbot for PageTurner Books, a fictional online bookstore. It is a CLI application — you run it in the terminal and type messages. Under the hood it uses the Claude API for everything.

The project is deliberately structured to show one Claude API feature per module. Here is the map:

```
config.py        →  Settings dataclass, system prompt
conversation.py  →  Multi-turn memory (stateless API workaround)
chat.py          →  Main orchestrator: RAG + tool loop + streaming + prefill
tools.py         →  Tool definitions, schemas, executor
rag.py           →  Chunking, embeddings, vector search, BM25, hybrid RRF
output.py        →  Streaming, structured JSON extraction
media.py         →  Image and PDF input
main.py          →  CLI loop, slash commands
```

Every feature is wired together into a single coherent application so you can see how they interact in practice — not just toy examples.

---

## 2. Startup Sequence

When you run `python main.py`, three things happen before you can type a single message:

```python
# main.py

settings = Settings.from_env()          # 1. load config
rag = RAGIndex()
rag.build(POLICY_PATH, settings.voyage_api_key)  # 2. build RAG index
bot = HelpBot(settings=settings, rag_index=rag)  # 3. create bot instance
```

**Why this order matters:**

`Settings` must come first because the API keys are needed by everything else. If `ANTHROPIC_API_KEY` is not set, `Settings.from_env()` raises `EnvironmentError` and the program exits immediately with a clear message — better than a cryptic auth error deep inside a later call.

`RAGIndex.build()` must happen before any user message, because it does the expensive work: reading the policy document, splitting it into sections, and sending all sections to Voyage AI to get embedding vectors. This is a one-time cost at startup. If it ran on every query, the first word of every message would be delayed by an embedding API call.

`HelpBot` is created last because it needs both the settings (for the Anthropic API key and model name) and the already-built RAG index. One `HelpBot` instance represents one customer session — it owns the conversation history for the duration.

---

## 3. Settings and Configuration

`config.py` contains two things: the `Settings` dataclass and the `SYSTEM_PROMPT` string.

```python
# helpbot/config.py

@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 1000
    temperature: float = 0.3
    voyage_api_key: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        key = os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. "
                "Copy .env.example to .env and add your key."
            )
        return cls(
            anthropic_api_key=key,
            voyage_api_key=os.getenv("VOYAGE_API_KEY", ""),
        )
```

`frozen=True` means every field is set once at creation and then read-only. Attempting `settings.model = "something-else"` would raise a `FrozenInstanceError`. This is intentional — API keys and model names should never change during a session.

Notice that `temperature` is a field on `Settings` but also a mutable property on `HelpBot`. The `Settings` value is just the default at startup. When the user types `/temp warm`, that only changes `bot.temperature` — not `settings.temperature`. The `Settings` object acts as the initial config snapshot.

`voyage_api_key` defaults to an empty string. If it's not set, `RAGIndex.build()` will catch the error gracefully and disable RAG — HelpBot still works, it just won't retrieve policy context before answering.

---

## 4. The System Prompt

The system prompt is the instruction Claude receives before any conversation starts. It defines the bot's identity, personality, rules, and constraints.

```python
# helpbot/config.py

SYSTEM_PROMPT = """\
Act as HelpBot, PageTurner Books' customer support agent. \
Your job is to resolve customer issues efficiently and warmly.

Your personality:
- Warm and approachable, like a knowledgeable bookshop employee
- You occasionally use gentle book-related metaphors \
("Let's get to the final chapter of this issue...")
- You never fabricate information — if you don't know, say so honestly
- You always provide a concrete next step or a clear escalation path

When handling a complaint:
1. Acknowledge the customer's frustration genuinely (not just "I understand")
2. Identify the specific issue (order, product quality, shipping)
3. Provide a concrete next step, not vague promises
4. If you cannot resolve it, explain clearly who can and how to reach them

You can help with: order tracking, returns, account issues, bookstore questions.
You cannot: process payments or modify orders directly.
Always greet the customer by name if they share it.

When answering policy questions, use ONLY the information in <policy_context> \
when present. If the answer is not there, say so — do not guess.

<example>
User: My book arrived with a ripped cover.
HelpBot: Oh no — a damaged book is such a disappointment, especially when \
you're excited to read it. I'll get this sorted right away. Could you share \
your order number so I can arrange a replacement or refund, whichever you prefer?
</example>
"""
```

Several design decisions are worth understanding here:

**"You never fabricate information"** — this is the honesty constraint. Without it, Claude might confidently invent a return policy ("you have 60 days") that contradicts your actual policy. LLMs are trained to be helpful and will fill gaps with plausible-sounding information if not instructed otherwise.

**"Use ONLY the information in `<policy_context>` when present"** — this is the RAG grounding rule. Every time the user asks a policy question, the RAG system retrieves relevant sections from the actual policy document and wraps them in `<policy_context>` tags. This rule tells Claude to treat those tags as the authoritative source and ignore its training data for those questions.

**The `<example>` block** — this is a one-shot example. Showing Claude a sample interaction is more effective than describing the desired tone in the abstract. Claude pattern-matches on the example and produces similar responses. The example demonstrates: empathy before action, concrete next step, warm language.

**The numbered complaint-handling steps** — these create a reliable structure for Claude to follow. Instead of sometimes acknowledging and sometimes jumping straight to solutions, Claude always works through the steps in order.

---

## 5. Prompt Caching

Every time you send a message to Claude, you pay for every input token — including the system prompt, the full conversation history, and all the tool schemas. In a long conversation, the system prompt alone might be 500+ tokens sent 20+ times, meaning you pay for 10,000+ tokens that never change.

Prompt caching solves this. When you mark a block with `cache_control`, Anthropic stores it server-side after the first request. Subsequent requests that include the same block pay roughly 10% of the normal input token price for those tokens.

```python
# helpbot/chat.py

_CACHED_SYSTEM = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]
```

The system prompt is turned from a plain string into a list containing one content block with `cache_control` attached. This is the format the API expects for cacheable system content.

The tool schemas are also cached — notice the last entry in `TOOL_SCHEMAS` in `tools.py`:

```python
# helpbot/tools.py  (last tool schema)
{
    "name": "get_estimated_restock_date",
    "description": "...",
    "input_schema": { ... },
    "cache_control": {"type": "ephemeral"},   # <-- caches all three tool schemas
}
```

Putting `cache_control` on the **last** tool is intentional. The cache applies to everything up to and including that point in the input — so placing it on the last tool caches all three tool definitions as one unit.

**Reading the token stats:** After every reply you'll see:

```
[tokens  in=1823  out=142  cache_read=1650  cache_write=0  temp=0.3]
```

On the very first turn you'll see `cache_write=1650, cache_read=0` — the cache is being written. On every turn after that, `cache_read=1650, cache_write=0` — you're reading from cache. The `in=1823` includes the cache_read tokens, but they are billed at ~10% of the normal rate, so the actual cost is much lower than the token count suggests.

---

## 6. Conversation History

The Claude API is completely stateless. It has no concept of a "session" or "conversation" — every API call is independent. When you send a message, Claude has no memory of anything you said before unless you include it in the request.

This means your application is responsible for maintaining the full conversation history and sending it with every request.

```python
# helpbot/conversation.py

@dataclass
class Conversation:
    _messages: list[dict[str, Any]] = field(default_factory=list)

    def add_user(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})

    def add_assistant(self, text: str) -> None:
        self._messages.append({"role": "assistant", "content": text})

    def add_assistant_raw(self, content: Any) -> None:
        self._messages.append({"role": "assistant", "content": content})

    def add_tool_results(self, results: list[dict[str, Any]]) -> None:
        self._messages.append({"role": "user", "content": results})

    def pop_last(self) -> dict[str, Any]:
        return self._messages.pop()
```

After a three-turn conversation, the `_messages` list looks like this:

```python
[
    {
        "role": "user",
        "content": "<policy_context>...</policy_context>\n\nCustomer question: Where is my order PT-9923?"
    },
    {
        "role": "assistant",
        "content": "Your order PT-9923 has shipped via FedEx and arrives tomorrow by 8 pm."
    },
    {
        "role": "user",
        "content": "<policy_context>...</policy_context>\n\nCustomer question: Can I return it?"
    },
    {
        "role": "assistant",
        "content": "Good news — PT-9923 was placed on 2026-05-20, so you're still within the 30-day return window."
    },
    {
        "role": "user",
        "content": "What if I lost the packaging?"
    }
]
```

This entire list is sent to Claude on every API call. Claude reads the full history and responds in context.

**Why `add_tool_results` uses the `user` role:** When Claude calls a tool, the results must be sent back in a `user` role message. This is the API convention — Claude "speaks" the tool call (as an `assistant` turn), and you "respond" with the result (as a `user` turn). It may feel counterintuitive but the alternating user/assistant structure is required by the API.

**Why `add_assistant_raw` exists separately from `add_assistant`:** During tool use, Claude's response content is not a simple string — it's a list of blocks that may include `text` blocks and `tool_use` blocks mixed together. `add_assistant_raw` stores the raw content as-is. `add_assistant` is for simple string replies.

**`pop_last`** is used in two places: during the prefill flow (see section 12) and when replacing a non-streaming tool-loop entry with a streaming one (see section 9).

---

## 7. A Full Chat Turn — Step by Step

Let's trace exactly what happens when you type `"Where is my order PT-9923?"`.

### Step 1: The input reaches `main.py`

```python
# main.py — main loop

user_input = input("You: ").strip()   # "Where is my order PT-9923?"
lower = user_input.lower()

# Not a slash command, not "return", not "quit" — falls through to:
result = bot.chat(user_input)
```

### Step 2: `HelpBot.chat()` is called

```python
# helpbot/chat.py

def chat(self, user_input: str) -> StreamResult:
    augmented = self._augment_with_rag(user_input)
    self._conversation.add_user(augmented)
    return self._run_turn()
```

Two things happen before the API is even contacted: RAG augmentation and adding to history.

### Step 3: RAG augmentation

```python
def _augment_with_rag(self, text: str) -> str:
    chunks = self._rag.search(text, self._settings.voyage_api_key)
    if not chunks:
        return text
    context = "\n\n---\n\n".join(chunks)
    return (
        f"<policy_context>\n{context}\n</policy_context>\n\n"
        f"Customer question: {text}"
    )
```

The RAG index searches for the most relevant sections of the policy document. For "Where is my order PT-9923?", it might retrieve the "Order Tracking" and "Shipping" sections.

The message sent to Claude actually looks like this:

```
<policy_context>
## Order Tracking
You can track your order using the tracking number emailed to you at dispatch.
Orders typically ship within 1-2 business days...

---

## Shipping
Standard shipping takes 3-5 business days. Express shipping is available...
</policy_context>

Customer question: Where is my order PT-9923?
```

This is the message that gets added to conversation history and sent to Claude. The `<policy_context>` tags wrap the retrieved content, and the system prompt's rule ("use ONLY the information in `<policy_context>`") ensures Claude relies on this retrieved text rather than guessing.

### Step 4: First API call — Claude decides to use a tool

```python
def _call(self) -> Any:
    return self._client.messages.create(
        model=self._settings.model,
        max_tokens=self._settings.max_tokens,
        system=_CACHED_SYSTEM,
        messages=self._conversation.messages,
        tools=TOOL_SCHEMAS,
        temperature=self._temperature,
    )
```

Claude receives the system prompt, the conversation history (with the augmented user message), and the tool schemas. It understands the customer is asking about an order, recognises that `check_order_status` is the right tool, and responds:

```python
response.stop_reason  # → "tool_use"
response.content      # → [
#     TextBlock(type="text", text="Let me check that order for you."),
#     ToolUseBlock(type="tool_use", id="tu_xyz", name="check_order_status",
#                  input={"order_id": "PT-9923"})
# ]
```

### Step 5: Store Claude's tool request in history

```python
self._conversation.add_assistant_raw(response.content)
```

The raw content (including the `tool_use` block) is stored in history. This is required — when you send the tool result back, Claude needs to see its own previous tool request to match the `tool_use_id`.

### Step 6: Execute the tool

```python
tool_results = execute_tool_calls(response.content)
self._conversation.add_tool_results(tool_results)
```

`execute_tool_calls` loops through the response content blocks, finds the `tool_use` block, looks up `check_order_status` in `_REGISTRY`, and calls it with `order_id="PT-9923"`.

```python
# helpbot/tools.py

_ORDERS = {
    "PT-9923": {
        "status": "shipped",
        "carrier": "FedEx",
        "eta": "Tomorrow by 8 pm",
        "order_date": "2026-05-20",
    },
    ...
}

def check_order_status(order_id: str) -> dict[str, Any]:
    _validate_order_id(order_id)
    order = _ORDERS.get(order_id)
    if order is None:
        return {"status": "not_found", "message": f"No order found for {order_id}."}
    return {k: v for k, v in order.items() if k != "order_date"}
```

The result `{"status": "shipped", "carrier": "FedEx", "eta": "Tomorrow by 8 pm"}` is JSON-serialized and added to the conversation as:

```python
{
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "tu_xyz",
            "content": '{"status": "shipped", "carrier": "FedEx", "eta": "Tomorrow by 8 pm"}',
            "is_error": False
        }
    ]
}
```

### Step 7: Second API call — Claude has the result

The `while True` loop sends the conversation to Claude again. Claude now sees its own tool request and the result. Since there are no more tools to call, it responds with `stop_reason = "end_turn"`.

The code detects this:

```python
if response.stop_reason != "tool_use":
    # Done with tools — replace the non-streamed entry and stream the final reply
    self._conversation.pop_last()
    ...
    result = stream_reply(...)
    ...
    return result
```

### Step 8: Stream the final reply

The previous non-streaming assistant turn is removed (`pop_last()`), and a new streaming call produces the final reply word-by-word. See section 9 for streaming details.

### Step 9: Store and display token stats

```python
self._conversation.add_assistant(result.text)
```

The streamed reply is stored in history. Back in `main.py`:

```python
print(
    f"  [tokens  in={result.input_tokens}"
    f"  out={result.output_tokens}"
    f"  cache_read={result.cache_read_tokens}"
    f"  cache_write={result.cache_write_tokens}"
    f"  temp={bot.temperature}]\n"
)
```

---

## 8. Tool Use — How Claude Calls Functions

Tool use is one of the most important Claude API features. It lets Claude decide when to fetch real data instead of guessing.

### What a tool schema looks like

```python
# helpbot/tools.py

{
    "name": "check_order_status",
    "description": (
        "Looks up the current shipping and delivery status of a PageTurner order. "
        "Call this when a customer asks where their order is, when it arrives, "
        "or whether it has been delivered."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "PageTurner order ID in the format PT-XXXX (e.g. PT-9923).",
            }
        },
        "required": ["order_id"],
    },
}
```

The `description` field is critical — it tells Claude **when** to call this tool, not just what it does. Claude reads all the descriptions and decides which tool, if any, fits the situation. A vague description leads to wrong tool selection or missed tool calls.

The `input_schema` is a JSON Schema object. Claude uses this to know what arguments to provide. The `required` array tells Claude which fields it must always include.

### The tool loop in full detail

```python
# helpbot/chat.py

def _run_turn(self) -> StreamResult:
    while True:
        response = self._call()
        self._conversation.add_assistant_raw(response.content)

        if response.stop_reason != "tool_use":
            # Claude is done calling tools — stream the final reply
            self._conversation.pop_last()

            if self._prefill:
                self._conversation.add_assistant(self._prefill)

            result = stream_reply(
                client=self._client,
                model=self._settings.model,
                system=_CACHED_SYSTEM,
                messages=self._conversation.messages,
                tools=TOOL_SCHEMAS,
                temperature=self._temperature,
                prefill=self._prefill,
            )

            if self._prefill:
                self._conversation.pop_last()

            self._conversation.add_assistant(result.text)
            return result

        tool_results = execute_tool_calls(response.content)
        self._conversation.add_tool_results(tool_results)
```

The loop runs until `stop_reason != "tool_use"`. Claude may call multiple tools across multiple iterations before giving its final answer. For example, if a customer says "Is my order PT-9923 eligible for return?", Claude might call both `check_order_status` and `check_return_eligibility` before responding.

Each iteration adds to the conversation:
- Claude's tool request (assistant turn with `tool_use` block)
- Your tool result (user turn with `tool_result` block)

By the time Claude gives its final answer, the history includes the complete tool exchange, which Claude uses to construct an accurate, grounded reply.

### The tool executor

```python
# helpbot/tools.py

def execute_tool_calls(blocks: list[Any]) -> list[dict[str, Any]]:
    results = []

    for block in blocks:
        if block.type != "tool_use":
            continue

        fn = _REGISTRY.get(block.name)
        if fn is None:
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Tool '{block.name}' is not available.",
                "is_error": True,
            })
            continue

        try:
            output = fn(**block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(output),
                "is_error": False,
            })
        except Exception:
            log.exception("Tool '%s' raised an exception", block.name)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Tool '{block.name}' failed. Please try again.",
                "is_error": True,
            })

    return results
```

Three things to notice:

1. **`block.input` is unpacked with `**`** — the tool schema's `input_schema` defines the exact parameter names, so `fn(**block.input)` calls the Python function with the right keyword arguments directly.

2. **Unknown tools return `is_error: True`** — Claude sees the error and can tell the user something went wrong rather than silently failing.

3. **`tool_use_id` links result to request** — each tool result must reference the `id` from the corresponding `tool_use` block. Without this, Claude cannot match results to requests when multiple tools are called in one turn.

### Return eligibility example — two tools in one turn

```
You: Can I return order PT-9923? It arrived damaged.

Claude calls: check_order_status("PT-9923")
  → {"status": "shipped", "carrier": "FedEx", "eta": "Tomorrow by 8 pm"}

Claude calls: check_return_eligibility("PT-9923")
  → {
      "eligible": true,
      "days_since_order": 25,
      "days_remaining": 5,
      "reason": "Order placed 25 days ago — within the 30-day return window."
    }

Claude responds: "Good news — your order PT-9923 is within the return window
  with 5 days remaining. Since the book arrived damaged, I can arrange a
  replacement or refund right away. Which would you prefer?"
```

---

## 9. Streaming Responses

Without streaming, the user types a message and then waits — possibly several seconds — before seeing any response. With streaming, each token appears as Claude generates it, making the bot feel immediate and alive.

```python
# helpbot/output.py

def stream_reply(
    client, model, system, messages, tools, temperature,
    on_token=None, prefill=""
) -> StreamResult:

    emit = on_token or (lambda chunk: print(chunk, end="", flush=True))

    if prefill:
        emit(prefill)   # print the prefill phrase before streaming starts

    streamed_text = ""

    with client.messages.stream(
        model=model,
        max_tokens=1000,
        system=system,
        messages=messages,
        tools=tools,
        temperature=temperature,
    ) as stream:
        for chunk in stream.text_stream:
            emit(chunk)             # print each token immediately
            streamed_text += chunk  # accumulate for history storage

        usage = stream.get_final_message().usage

    return StreamResult(
        text=prefill + streamed_text,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
        cache_write_tokens=getattr(usage, "cache_creation_input_tokens", 0) or 0,
    )
```

`client.messages.stream()` is a context manager that opens a persistent connection to the Claude API. `stream.text_stream` is a generator that yields text chunks. The `flush=True` argument to `print` forces the output buffer to flush immediately — without it, Python might batch the chunks and print them all at once.

**Why two separate calls — one non-streaming for tool use, one streaming for the final reply?**

Streaming and tool use interact in a complex way. During streaming, `stop_reason` is not known until the stream ends. If Claude decides mid-stream to call a tool, you'd have to interrupt the stream, handle the tool, and restart — creating a jarring experience. The cleaner approach used here: non-streaming calls for the tool loop (where speed doesn't matter because no text is being shown to the user), streaming only for the final human-facing reply (where speed matters most).

**The `on_token` callback** is an extension point. The default behaviour is printing to stdout, but any caller can pass a different function — for example, sending chunks over a WebSocket to a browser UI, writing to a log file, or buffering for tests.

**`StreamResult`** is a frozen dataclass that bundles the full text and token usage stats:

```python
@dataclass(frozen=True)
class StreamResult:
    text: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
```

`text` is `prefill + streamed_text` so the stored history entry is always complete regardless of whether prefill was active.

---

## 10. RAG — Retrieval-Augmented Generation

### The problem RAG solves

Claude's training data has a knowledge cutoff and doesn't include your company's specific policies. If you ask "What is PageTurner's return policy?", Claude might:
- Say it doesn't know (unhelpful)
- Make up a plausible-sounding policy that's wrong (dangerous)

RAG solves this by retrieving the actual policy text and giving it to Claude as context. Claude then answers based on what you gave it, not what it guessed.

### Step 1 — Chunking the document

```python
# helpbot/rag.py

def chunk_by_section(text: str) -> list[str]:
    raw = text.split("\n## ")
    chunks = []
    for i, section in enumerate(raw):
        section = section.strip()
        if not section:
            continue
        if i > 0:
            section = "## " + section
        chunks.append(section)
    return chunks
```

`pageturner_returns_policy.md` is split at every `## ` (H2 markdown header). The result is a list of self-contained sections, for example:

```
chunks[0] = "# PageTurner Returns Policy\nThis document outlines..."
chunks[1] = "## Returns\nYou may return any item within 30 days..."
chunks[2] = "## Damaged Items\nIf your book arrives damaged..."
chunks[3] = "## Shipping\nStandard delivery takes 3-5 business days..."
```

Splitting by section is better than splitting by fixed character count because each chunk is semantically coherent — a chunk about returns won't contain half a sentence about shipping that crossed a character boundary.

### Step 2 — Embedding (at startup)

```python
# helpbot/rag.py — inside RAGIndex.build()

client = voyageai.Client(api_key=voyage_api_key)
chunks = chunk_by_section(path.read_text(encoding="utf-8"))

embeddings = client.embed(texts=chunks, model="voyage-3").embeddings

for chunk, vector in zip(chunks, embeddings):
    self._vector_store.add(vector, chunk)
self._bm25_store.index(chunks)
```

Each chunk is sent to Voyage AI's `voyage-3` model. The model converts each chunk of text into a list of ~1024 floating-point numbers called an **embedding vector**. This vector encodes the semantic meaning of the text in a way that math can operate on.

Two chunks with similar meaning will have similar vectors (their cosine similarity will be close to 1.0). Two chunks about completely different topics will have dissimilar vectors (cosine similarity close to 0).

This embedding step runs once at startup and the vectors are stored in memory. Future queries embed only the query text (a single small call) and then compare against the stored chunk vectors locally — no network call per query to retrieve, only to embed the query.

### Step 3 — Vector Store (cosine similarity)

```python
# helpbot/rag.py

class VectorStore:
    def search(self, query_vector: list[float], top_k: int = 3) -> list[str]:
        if not self._vectors:
            return []
        q = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q)
        scores = [
            float(np.dot(q, v) / (q_norm * np.linalg.norm(v) + 1e-10))
            for v in self._vectors
        ]
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self._docs[i] for i in top_indices[:top_k]]
```

Cosine similarity measures the angle between two vectors. A score of 1.0 means the vectors point in exactly the same direction (identical meaning). A score of 0.0 means they are perpendicular (unrelated).

For the query `"Where is my order PT-9923?"`:
- The "Order Tracking" section might score `0.87`
- The "Shipping" section might score `0.72`
- The "Returns" section might score `0.34`
- The "Gift Cards" section might score `0.11`

The top-2 chunks (Order Tracking and Shipping) would be returned.

**Why numpy instead of a vector database?** For a single small document like this policy file, a few dozen chunks at most, numpy cosine similarity is instant. A vector database (Pinecone, Weaviate, etc.) adds network latency and operational complexity that isn't justified at this scale.

### Step 4 — BM25 Keyword Store

```python
# helpbot/rag.py

class BM25Store:
    def index(self, docs: list[str]) -> None:
        from rank_bm25 import BM25Okapi
        self._docs = docs
        self._bm25 = BM25Okapi([doc.lower().split() for doc in docs])

    def search(self, query: str, top_k: int = 3) -> list[str]:
        if self._bm25 is None:
            return []
        scores = self._bm25.get_scores(query.lower().split())
        top_indices = scores.argsort()[-top_k:][::-1]
        return [self._docs[i] for i in top_indices]
```

BM25 (Best Match 25) is a classic information retrieval algorithm. It ranks documents by how often the query words appear in them, adjusted for document length (so a long section isn't unfairly rewarded just for being long).

BM25 catches cases where the exact query word is in the chunk but the semantic similarity is lower — for example, if a customer types a product ID or a specific phrase that appears verbatim in the policy.

### Step 5 — Hybrid Search with Reciprocal Rank Fusion

```python
# helpbot/rag.py — inside RAGIndex.search()

semantic = self._vector_store.search(query_vector, top_k=top_k)
keyword = self._bm25_store.search(query, top_k=top_k)

scores: dict[str, float] = {}
for rank, doc in enumerate(semantic):
    scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)
for rank, doc in enumerate(keyword):
    scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)

return sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]
```

Neither method alone is best in all cases. Semantic search finds conceptually related chunks even when the words differ. Keyword search catches exact term matches that semantic search might rank lower.

**Reciprocal Rank Fusion (RRF)** merges the two result lists without needing to normalize their scores onto the same scale (which is tricky because cosine similarity and BM25 use different numeric ranges):

- Semantic result #1: score += `1/(1+0)` = `1.0`
- Semantic result #2: score += `1/(1+1)` = `0.5`
- Keyword result #1: score += `1/(1+0)` = `1.0`
- Keyword result #2: score += `1/(1+1)` = `0.5`

If the "Returns" section is ranked #1 by both semantic and keyword search, it scores `1.0 + 1.0 = 2.0`. A section that only appears in one list scores at most `1.0`. This naturally boosts chunks that both methods agree on — which are almost always the right answers.

---

## 11. Structured Output — The Return Request Form

Type `return` and the conversation enters a completely different mode. Instead of a chat reply, the bot prompts for a free-text description of the return and extracts a structured JSON form from it.

This uses two Claude API techniques together: **prefilling** and **stop sequences**.

### The problem with asking for JSON naively

If you just say `"Respond in JSON"`, Claude might write:

```
Sure! Here is the return request in JSON format:

```json
{
  "order_id": "PT-9923",
  ...
}
```

I hope that helps!
```

Now you need to strip the explanation, find the JSON block, extract it, and parse it. This is fragile — Claude's exact phrasing varies.

### The solution: prefill + stop sequence

```python
# helpbot/output.py

response = client.messages.create(
    model=model,
    max_tokens=300,
    messages=[
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "```json"},   # ← prefill
    ],
    stop_sequences=["```"],                             # ← stop sequence
)
```

**Prefill** (`"```json"`): By adding a partial `assistant` message, you are telling Claude "you already started your reply with this". Claude must continue from exactly this point. It cannot write any preamble — the only valid continuation is the JSON content inside the code block.

**Stop sequence** (`"```"`): This tells Claude to stop generating the moment it produces the closing backticks. The response will never include anything after the JSON.

The result of `response.content[0].text` will always look like:
```
\n{\n  "order_id": "PT-9923",\n  ...}\n
```

Never with explanation, never with markdown formatting around it.

```python
raw = "```json" + response.content[0].text
return json.loads(raw.replace("```json", "").replace("```", "").strip())
```

The prefill is stitched back on (since it was added by you, not returned by the API), then stripped, and parsed as JSON. The result is always a clean Python dict.

### Example

```
[Return Request]
Describe your return — include order ID, reason, and urgency:
You: Order PT-9923, the cover is ripped and pages are falling out, this is urgent,
     I'd like a refund

--- Return Request Filed ---
{
  "order_id": "PT-9923",
  "reason": "torn cover and loose pages",
  "urgency": "high",
  "customer_name": null,
  "preferred_resolution": "refund"
}
----------------------------
```

Claude extracted structured data from free-form text — order ID, reason, urgency level, preferred resolution — without the customer needing to fill out a form.

---

## 12. Response Prefilling

Prefilling forces Claude to start every response with a specific phrase. This is useful for:

- **Tone control:** `/prefill I sincerely apologize` — every reply opens with an apology, useful for escalation situations
- **Format control:** `/prefill Here are my top 3 recommendations:` — forces a list format
- **Brand voice:** `/prefill Great news —` — ensures an upbeat opener for positive situations

### How it works in the API

The Claude API allows you to add a partial `assistant` turn at the end of the messages list. Claude treats this as text it already wrote and continues from it. It cannot go back and change the opening — it must continue from whatever you put there.

### The implementation — the `pop_last()` dance

```python
# helpbot/chat.py — inside _run_turn()

# Step 1: Replace the non-streamed entry that captured Claude's tool decisions
self._conversation.pop_last()

# Step 2: Add the prefill as a partial assistant turn
if self._prefill:
    self._conversation.add_assistant(self._prefill)

# Step 3: Stream — Claude continues from the prefill phrase
result = stream_reply(
    ...
    prefill=self._prefill,
)

# Step 4: Remove the partial prefill entry
if self._prefill:
    self._conversation.pop_last()

# Step 5: Store the complete reply (prefill + streamed text) as one entry
self._conversation.add_assistant(result.text)
```

The temporary entry in step 2 is needed so the API call includes the partial assistant turn. After streaming, it's removed in step 4, and the complete response (`prefill + streamed content`) is stored as a single clean entry in step 5.

Without this dance, the history would have two entries: one with just the prefill phrase and one with the streamed content — which would confuse Claude on the next turn since it would look like Claude said the phrase, stopped, and then said something else.

### In `stream_reply`

```python
# helpbot/output.py

if prefill:
    emit(prefill)   # print the prefill phrase to terminal before streaming

for chunk in stream.text_stream:
    emit(chunk)
```

The prefill is printed first so the user sees an uninterrupted flow:

```
HelpBot: I sincerely apologize — that delay is completely unacceptable...
         ^^^^^^^^^^^^^^^^^^^^^^^
         prefill printed here    streaming continues seamlessly
```

### Example

```
You: /prefill I sincerely apologize for the inconvenience —
  [prefill set → "I sincerely apologize for the inconvenience —"]

You: My order arrived three weeks late and I had it as a gift.
HelpBot: I sincerely apologize for the inconvenience — that must have been
         especially frustrating given the occasion. A three-week delay is not
         the standard we hold ourselves to. Let me look into order PT-... right away.
  [tokens  in=2041  out=89  cache_read=1650  cache_write=0  temp=0.3]
```

---

## 13. Image Input

```
You: /image photos/damaged_cover.jpg
```

Claude can read images natively. The image is encoded and sent as part of the message content alongside a text prompt.

### How the API call is structured

```python
# helpbot/media.py

def ask_about_image(client, model, image_path, question) -> str:
    path = Path(image_path)
    mime = _MIME_MAP.get(path.suffix.lstrip(".").lower(), "image/jpeg")

    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime,
                        "data": base64.standard_b64encode(path.read_bytes()).decode("utf-8"),
                    },
                },
                {
                    "type": "text",
                    "text": question,
                },
            ],
        }],
    )
    return response.content[0].text
```

The key difference from a regular message: the `content` field is a **list of blocks** instead of a plain string. Each block is either `"type": "image"` or `"type": "text"`. Claude receives them together and answers the text question in the context of the image.

The image is base64-encoded — the raw bytes of the file are converted to a text-safe string and embedded directly in the JSON request body. No file upload, no URL — the image travels inside the API call itself.

Supported formats: JPEG, PNG, WebP, GIF. The `_MIME_MAP` dict handles the extension-to-MIME-type translation.

### The question sent to Claude for damage categorisation

```python
question = (
    "You are a customer support agent for PageTurner Books. "
    "A customer has sent a photo of their book. "
    f"Categorise the damage into exactly one of: {_DAMAGE_CATEGORIES}. "
    "Then write a 1-sentence description of what you see. "
    "Reply in this format:\n"
    "Category: <category>\nDescription: <description>"
)
```

The question is highly structured — it gives Claude the context (customer support scenario), the exact categories to choose from, and the exact output format required. Specific instructions produce consistent output.

### Connecting the analysis to the conversation

```python
# main.py

analysis = ask_about_image(client=bot._client, model=settings.model,
                           image_path=path, question=question)

print(f"\nHelpBot (image analysis):\n{analysis}\n")

damage_summary = f"[Customer attached a photo of their book. Analysis: {analysis}]"
result = bot.chat(
    f"{damage_summary}\n\nPlease acknowledge the damage and ask for their order ID "
    "so I can arrange a replacement or refund."
)
```

The image analysis result is injected back into the main conversation as a text message. This bridges the one-off image analysis call (which has no conversation history) with the ongoing support thread. Claude can then acknowledge the specific damage and ask for the order ID — maintaining continuity across both the image analysis and the follow-up chat.

### Example session

```
You: /image photos/cover.jpg

[Analysing image: cover.jpg]

HelpBot (image analysis):
Category: torn cover
Description: The front cover has a large diagonal tear running from the top
             spine corner to the centre of the cover.

HelpBot: Oh no — a torn cover is such a disappointing way to receive a book.
         I can see from the photo that the damage is quite significant. Could
         you share your order number so I can arrange a replacement or refund,
         whichever you prefer?
  [tokens  in=1944  out=67  cache_read=1650  cache_write=0  temp=0.3]
```

---

## 14. Temperature Control

Temperature is a parameter that controls how Claude samples its responses. At every step, Claude calculates a probability distribution over all possible next tokens. Temperature adjusts that distribution:

- **Low temperature (0.0–0.3):** The distribution is sharpened — the most probable token is heavily favoured. Claude picks almost the same tokens every time. Responses are consistent, predictable, factual.
- **High temperature (0.7–1.0):** The distribution is flattened — lower-probability tokens get more weight. Claude samples more broadly. Responses are varied, sometimes surprising, more creative.

### The four presets explained

```python
_TEMP_PRESETS = {
    "precise":  (0.1, "order lookups — consistent, factual"),
    "support":  (0.3, "standard support — default"),
    "warm":     (0.7, "apology emails — more human-feeling"),
    "creative": (0.9, "book recommendations — varied & surprising"),
}
```

**`precise` (0.1):** Order lookups have one right answer — the actual order status. You want Claude to report facts, not paraphrase them differently each time. Low temperature ensures the factual core is always present.

**`support` (0.3):** The default. Warm enough to feel human, consistent enough to be reliable. Most support interactions land here.

**`warm` (0.7):** Apology emails benefit from slight variation. If every apology sounds identical, it feels robotic. A little randomness makes "I sincerely apologize" sound less like a template.

**`creative` (0.9):** Book recommendations are inherently subjective. High temperature means Claude will suggest different books each time, explore different angles, and occasionally make unexpected connections — all desirable for a recommendation engine.

### The implementation

```python
# helpbot/chat.py

@property
def temperature(self) -> float:
    return self._temperature

@temperature.setter
def temperature(self, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"Temperature must be between 0.0 and 1.0, got {value}")
    self._temperature = value
```

Temperature is a validated property on `HelpBot`. The setter rejects values outside the valid range instead of silently sending an invalid parameter to the API.

### Try it yourself

```
You: /temp precise
You: What is the status of order PT-9923?
```
Run this twice — the answer will be nearly identical both times.

```
You: /temp creative
You: Can you recommend a book similar to Project Hail Mary?
```
Run this twice — you'll get different books and different reasoning each time.

---

## 15. Full Conversation Trace

Here is a realistic multi-feature conversation with annotations showing what happens internally at each step.

```
============================================================
  PageTurner Books — Customer Support (HelpBot)
============================================================
  Temperature : 0.3  (/temp <0.0–1.0> or preset)
  Presets     : /temp precise · support · warm · creative
  Prefill     : off  (/prefill <phrase> | /prefill off)
  Commands    : 'return' · /image <path> · 'quit'
------------------------------------------------------------
```

---

```
You: Hi, my name is Priya and my book arrived damaged.
```
**Internally:**
- RAG retrieves: "Damaged Items" section from the policy doc
- Augmented message: `<policy_context>## Damaged Items\n...</policy_context>\n\nCustomer question: Hi, my name is Priya...`
- No tool call needed — Claude replies from context + personality
- System prompt rule: "Always greet the customer by name if they share it"

```
HelpBot: Hi Priya! Oh no — a damaged book is such a disappointment. I'm so
         sorry that happened. Could you tell me a bit more about the damage,
         and share your order number so I can look into this right away?
  [tokens  in=2103  out=51  cache_read=1650  cache_write=412  temp=0.3]
```
*(First turn: `cache_write=412` — system prompt + tool schemas written to cache)*

---

```
You: Order PT-9923. The cover is completely torn.
```
**Internally:**
- RAG retrieves: "Damaged Items" and "Returns" sections
- Claude decides to call two tools: `check_order_status("PT-9923")` and `check_return_eligibility("PT-9923")`
- Tool loop runs twice
- `check_order_status` returns: `{status: "shipped", carrier: "FedEx", eta: "Tomorrow by 8 pm"}`
- `check_return_eligibility` returns: `{eligible: true, days_since_order: 25, days_remaining: 5}`
- Claude streams final reply

```
HelpBot: Thank you, Priya. I can see your order PT-9923 shipped via FedEx
         and is due tomorrow. You're within the return window with 5 days
         remaining, so we can absolutely sort this out. Would you prefer a
         replacement copy or a full refund?
  [tokens  in=2387  out=73  cache_read=2062  cache_write=0  temp=0.3]
```
*(Cache read now includes system prompt + tools — 0 write cost)*

---

```
You: /image photos/torn_cover.jpg
```
**Internally:**
- Image read from disk, base64-encoded
- Separate API call to `ask_about_image` (not part of conversation history)
- Claude analyses the image against the damage categories
- Analysis result injected into main conversation as a text message
- `bot.chat()` called with the injected finding

```
[Analysing image: torn_cover.jpg]

HelpBot (image analysis):
Category: torn cover
Description: A large diagonal tear runs from the top-left corner to the middle
of the front cover, with partial separation from the spine.

HelpBot: I can clearly see the damage, Priya — that tear is significant and
         the book should never have left our warehouse in that condition. I've
         noted it as a torn cover in your case file. Shall I process a
         replacement now, or would you prefer the refund?
  [tokens  in=2519  out=62  cache_read=2062  cache_write=0  temp=0.3]
```

---

```
You: return
```

```
[Return Request]
Describe your return — include order ID, reason, and urgency:
You: PT-9923, the cover is torn badly, I need this resolved today, refund please
```
**Internally:**
- `extract_return_request()` called
- Prefill `"```json"` + stop sequence `"```"` technique used
- Claude extracts structured data from the free-text description

```
--- Return Request Filed ---
{
  "order_id": "PT-9923",
  "reason": "torn cover",
  "urgency": "high",
  "customer_name": null,
  "preferred_resolution": "refund"
}
----------------------------

HelpBot: I've logged your return for order PT-9923. You'll receive a
         confirmation email within 24 hours.
```

---

```
You: /prefill Wonderful news, Priya —
  [prefill set → "Wonderful news, Priya —"]

You: Is Atomic Habits in stock?
```
**Internally:**
- RAG retrieves inventory-related policy sections
- Claude calls `get_estimated_restock_date("Atomic Habits")`
- Tool returns: `{found: true, in_stock: true, message: "Atomic Habits is currently in stock and ready to ship."}`
- Prefill injected before streaming

```
HelpBot: Wonderful news, Priya — Atomic Habits is currently in stock and
         ready to ship. Would you like to place an order?
  [tokens  in=2601  out=34  cache_read=2062  cache_write=0  temp=0.3]
```

---

```
You: quit
HelpBot: Thanks for contacting PageTurner. Happy reading!
```

---

## Summary

The project demonstrates eight Claude API features working together:

| Feature | File | Key concept |
|---|---|---|
| System prompt | `config.py` | Defines identity, rules, few-shot example |
| Prompt caching | `chat.py` | `cache_control` reduces cost on repeated tokens |
| Multi-turn memory | `conversation.py` | Full history sent with every stateless API call |
| Tool use | `tools.py`, `chat.py` | Claude requests → you execute → loop until done |
| Streaming | `output.py` | Token-by-token output via `messages.stream()` |
| RAG | `rag.py` | Chunk → embed → hybrid search → inject context |
| Structured output | `output.py` | Prefill + stop sequence forces clean JSON |
| Response prefill | `chat.py` | Partial assistant turn steers Claude's opening |
| Image input | `media.py` | Base64-encoded image block in message content |
| Temperature | `chat.py`, `main.py` | Controls randomness — low for facts, high for creativity |
