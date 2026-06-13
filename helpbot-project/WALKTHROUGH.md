# HelpBot — Project Walkthrough

This guide walks through the project from startup to a complete conversation, explaining what happens at each step and why the code is written the way it is. Read the `README.md` first for setup instructions and the command reference.

---

## 1. Startup — What Happens Before the First Message

Run `python main.py` and three things happen in sequence.

### 1a. Load Settings

```python
settings = Settings.from_env()
```

`Settings` is a **frozen dataclass** — all fields are set once and cannot change. API keys, model name, max tokens, and default temperature are all loaded here from your `.env` file. If `ANTHROPIC_API_KEY` is missing, the program exits immediately with a clear error rather than failing later mid-conversation.

Mutable state like temperature and prefill intentionally live on `HelpBot`, not `Settings` — they need to change mid-session while the keys should never change.

### 1b. Build the RAG Index

```python
rag = RAGIndex()
rag.build("pageturner_returns_policy.md", settings.voyage_api_key)
```

This reads `pageturner_returns_policy.md`, splits it into sections, and sends every section to Voyage AI to get an embedding vector. It also builds a BM25 keyword index from the same sections.

This happens **once at startup**, not per query. The cost is a one-time API call to Voyage. Every subsequent query just does fast local math (cosine similarity + BM25 scoring) to find the right section.

### 1c. Create the Bot

```python
bot = HelpBot(settings=settings, rag_index=rag)
```

`HelpBot` holds the Anthropic client, the conversation history, a reference to the RAG index, and the current temperature and prefill values. One instance per customer session.

---

## 2. The System Prompt and Prompt Caching

The system prompt is defined in `config.py` and tells Claude who it is, how to behave, and the rules it must follow.

```python
SYSTEM_PROMPT = """
Act as HelpBot, PageTurner Books' customer support agent...
When handling a complaint:
1. Acknowledge genuinely (not just "I understand")
2. Identify the specific issue
3. Provide a concrete next step
...
When answering policy questions, use ONLY the information in <policy_context>
when present. If the answer is not there, say so — do not guess.
"""
```

The last rule is critical for RAG to work correctly. Without it, Claude might answer policy questions from its training data instead of your actual policy document.

In `chat.py`, the system prompt is wrapped before being sent:

```python
_CACHED_SYSTEM = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]
```

The `cache_control` field tells Anthropic's servers to cache this block. After the first request, the system prompt tokens are stored server-side. Every subsequent turn reads from cache instead of re-processing the full prompt text.

**What this means in practice:** After your first message, you'll see `cache_read=1650` (or similar) in the token usage line. Those tokens cost about 10% of normal input token price. In a 20-turn conversation, that's roughly 17 turns of heavily discounted system prompt tokens.

---

## 3. A Regular Chat Turn — End to End

Type a message like `"Where is my order PT-9923?"` and trace what happens:

### Step 1: RAG Augmentation

```python
def _augment_with_rag(self, text: str) -> str:
    chunks = self._rag.search(text, self._settings.voyage_api_key)
    if not chunks:
        return text
    context = "\n\n---\n\n".join(chunks)
    return f"<policy_context>\n{context}\n</policy_context>\n\nCustomer question: {text}"
```

Before the message is sent to Claude, it's run through the RAG index. The index finds the most relevant policy sections and prepends them. For an order status question, the retrieved chunks might include the "Order Tracking" and "Shipping" sections of the policy doc.

The `<policy_context>` tags are significant — the system prompt explicitly tells Claude to use only what's inside those tags for policy questions.

### Step 2: Add to Conversation History

```python
self._conversation.add_user(augmented)
```

The `Conversation` class holds the full message list. The Claude API is stateless — it has no memory between calls. Every single request sends the complete history from the beginning. The `Conversation` class is the single place that manages this list.

```python
# What gets sent to Claude every turn:
[
    {"role": "user", "content": "<policy_context>...</policy_context>\n\nCustomer question: Where is my order PT-9923?"},
    {"role": "assistant", "content": "Let me check that for you..."},
    {"role": "user", "content": "Can I return it?"},
    # ... every prior turn
]
```

### Step 3: First API Call (Non-Streaming)

```python
response = self._client.messages.create(
    model=self._settings.model,
    max_tokens=self._settings.max_tokens,
    system=_CACHED_SYSTEM,
    messages=self._conversation.messages,
    tools=TOOL_SCHEMAS,
    temperature=self._temperature,
)
```

Claude receives the full conversation plus the tool schemas and decides what to do. For an order status question, Claude will respond with `stop_reason = "tool_use"` and a `tool_use` block requesting `check_order_status` with `order_id = "PT-9923"`.

This first call is **non-streaming** because handling tool use mid-stream adds significant complexity for no user-facing benefit.

### Step 4: Tool Execution

```python
tool_results = execute_tool_calls(response.content)
self._conversation.add_tool_results(tool_results)
```

`execute_tool_calls` loops through Claude's response blocks, finds every `tool_use` block, looks up the matching Python function in `_REGISTRY`, calls it, and returns the results. The results are added to the conversation as a `user` role message — this is the Claude API's convention for returning tool results.

```python
# What check_order_status("PT-9923") returns:
{
    "status": "shipped",
    "carrier": "FedEx",
    "eta": "Tomorrow by 8 pm"
}
```

This gets JSON-serialized and sent back to Claude.

### Step 5: Loop Back

The `while True` loop in `_run_turn` sends the conversation to Claude again, now including the tool result. Claude reads the result and this time responds with `stop_reason = "end_turn"` — meaning it's ready to give the final answer.

### Step 6: Streaming the Final Reply

```python
result = stream_reply(
    client=self._client,
    model=self._settings.model,
    system=_CACHED_SYSTEM,
    messages=self._conversation.messages,
    tools=TOOL_SCHEMAS,
    temperature=self._temperature,
    prefill=self._prefill,
)
```

```python
with client.messages.stream(...) as stream:
    for chunk in stream.text_stream:
        print(chunk, end="", flush=True)
        streamed_text += chunk
```

`text_stream` is an iterator that yields text chunks as Claude generates them. Each chunk is printed immediately — the user sees the reply appear word-by-word instead of waiting for the complete response.

After streaming finishes, `get_final_message().usage` gives the token counts including cache hits.

### Step 7: Store and Print Token Stats

```python
self._conversation.add_assistant(result.text)
```

The full reply is stored in conversation history so future turns have context. Then `main.py` prints:

```
[tokens  in=1823  out=142  cache_read=1650  cache_write=0  temp=0.3]
```

- `in` — total input tokens billed (includes history + system prompt)
- `out` — tokens Claude generated
- `cache_read` — tokens served from cache at ~10% cost (this is the system prompt)
- `cache_write` — tokens written to cache (only on the first turn)

---

## 4. How Tool Use Works

Claude does not call your functions directly. It outputs a structured request, you run the function, and you send the result back. The full exchange looks like this:

```
Turn 1 — You send:
  user: "Where is my order PT-9923?"
  [tools: check_order_status, check_return_eligibility, get_estimated_restock_date]

Turn 1 — Claude responds:
  stop_reason: "tool_use"
  content: [
    { type: "tool_use", id: "tu_abc", name: "check_order_status", input: { order_id: "PT-9923" } }
  ]

Turn 2 — You send (adding the result):
  user: [
    { type: "tool_result", tool_use_id: "tu_abc", content: '{"status":"shipped","carrier":"FedEx","eta":"Tomorrow by 8 pm"}' }
  ]

Turn 2 — Claude responds:
  stop_reason: "end_turn"
  content: "Your order PT-9923 is shipped via FedEx and arrives tomorrow by 8 pm."
```

Claude can also chain tool calls — it might call `check_order_status` and then `check_return_eligibility` before giving a final answer, running through the loop twice before stopping.

The tool schemas have `cache_control` on the last entry, which caches the entire tool list. This is important because tool schemas are verbose JSON and get sent on every turn.

---

## 5. How RAG Works

RAG stands for Retrieval-Augmented Generation. The idea is: instead of relying on Claude's training data to answer policy questions, you retrieve the actual relevant text from your document and give it to Claude directly.

### Chunking

```python
def chunk_by_section(text: str) -> list[str]:
    raw = text.split("\n## ")
    ...
```

The policy document is split at every `##` H2 header. Each section (Returns, Shipping, Damaged Items, etc.) becomes an independent chunk. Splitting by section is better than fixed character lengths because sections are semantically coherent — a chunk about returns won't be half-returns half-shipping.

### Embedding

At startup, each chunk is sent to Voyage AI's `voyage-3` model which converts text into a list of 1024 numbers (a vector). These numbers encode the semantic meaning of the text. Chunks with similar meaning will have similar vectors.

### Two-Index Hybrid Search

When a query comes in, the system runs two separate searches and combines them:

**Semantic search (VectorStore):** The query is embedded into a vector, then compared to every chunk's vector using cosine similarity. Finds chunks that are *conceptually similar* even if they use different words. If a customer asks "how long do I have to send something back?", it finds the returns section even though it never says "send back".

**Keyword search (BM25Store):** Splits the query into words and scores chunks by how often those words appear, adjusted for document length. Finds exact matches that semantic search might rank lower.

**Reciprocal Rank Fusion (RRF):** The two result lists are merged without needing to normalize their scores:

```python
scores: dict[str, float] = {}
for rank, doc in enumerate(semantic):
    scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)
for rank, doc in enumerate(keyword):
    scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)
```

A chunk ranked #1 by semantic gets `1/1 = 1.0`. If the same chunk is ranked #2 by BM25, it gets an additional `1/2 = 0.5`. Total score: `1.5`. A chunk that only appears in one list maxes out at `1.0`. This naturally boosts chunks that both methods agree on.

---

## 6. Structured Output — The Return Request Form

Type `return` and you enter a different flow. Instead of a conversation, the bot prompts you for a description and then extracts a clean JSON form from your free-text reply.

```python
response = client.messages.create(
    model=model,
    max_tokens=300,
    messages=[
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "```json"},   # prefill
    ],
    stop_sequences=["```"],
)
```

Two techniques work together here:

**Prefill:** By adding a partial `assistant` message with `"```json"`, Claude is forced to continue from that exact point. It cannot write any introductory text — it has to start directly inside a JSON block.

**Stop sequence:** `"```"` tells Claude to stop generating the moment it closes the code block. The result is always clean, parseable JSON with no wrapper text.

Without these two techniques, Claude might write `"Sure! Here is the JSON you requested:\n```json\n{...}\n```"` — which requires parsing. With them, the output is always just `{...}`.

```python
raw = "```json" + response.content[0].text
return json.loads(raw.replace("```json", "").replace("```", "").strip())
```

The response is stitched back together with the prefill and stripped, giving a clean dict.

Example output:
```json
{
  "order_id": "PT-9923",
  "reason": "torn cover",
  "urgency": "high",
  "customer_name": null,
  "preferred_resolution": "unknown"
}
```

---

## 7. Prefilling Conversation Responses

The `/prefill` command makes every reply start with a fixed phrase.

```
You: /prefill I sincerely apologize for the inconvenience —
You: My book arrived three weeks late.
HelpBot: I sincerely apologize for the inconvenience — that's a long wait and
         completely unacceptable. Let me look into this right away...
```

How it works in `chat.py`:

```python
# 1. Add a partial assistant turn to history
if self._prefill:
    self._conversation.add_assistant(self._prefill)

# 2. Stream — Claude continues from the prefill phrase
result = stream_reply(..., prefill=self._prefill)

# 3. Remove the bare prefill entry
if self._prefill:
    self._conversation.pop_last()

# 4. Store the complete reply (prefill + streamed text)
self._conversation.add_assistant(result.text)
```

The temporary partial entry is added just before the API call, then immediately removed after streaming. The history ends up with a single clean entry containing `prefill + full response`. The `pop_last()` dance exists because if you stored just the prefill and let streaming extend it, the duplicate entry would corrupt the conversation structure.

In `stream_reply`, the prefill is also printed before streaming starts so the user sees an uninterrupted flow:

```python
if prefill:
    emit(prefill)   # print immediately

for chunk in stream.text_stream:
    emit(chunk)     # then stream the rest
```

---

## 8. Image Input

```
You: /image photos/damaged_cover.jpg
```

```python
def ask_about_image(client, model, image_path, question):
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
                        "media_type": "image/jpeg",
                        "data": base64.standard_b64encode(path.read_bytes()).decode()
                    }
                },
                {"type": "text", "text": question}
            ]
        }]
    )
    return response.content[0].text
```

The message `content` field is a list instead of a string. Each item is a block — one image block and one text block. Claude reads both simultaneously and answers the text question about the image.

The image is sent as base64-encoded bytes embedded directly in the request. No URL, no file upload — the raw pixels go in the JSON body.

After Claude categorises the damage, the finding is injected into the main conversation:

```python
damage_summary = f"[Customer attached a photo. Analysis: {analysis}]"
result = bot.chat(f"{damage_summary}\n\nPlease acknowledge the damage and ask for their order ID...")
```

This keeps the image analysis connected to the ongoing support thread so HelpBot can follow up, ask for an order ID, and arrange a replacement — all in the same conversation.

---

## 9. Temperature in Practice

Temperature controls randomness. At `0.0`, Claude always picks the most probable next token — fully deterministic. At `1.0`, it samples more broadly — more creative but less predictable.

Try this sequence to feel the difference:

```
You: /temp precise
You: What is the status of order PT-9923?
```
Claude gives a direct, factual answer. Same phrasing every time.

```
You: /temp creative
You: Can you recommend a book similar to Project Hail Mary?
```
Claude gives a more expansive, varied answer. Run it twice and the recommendations differ.

The presets map practical use-cases to appropriate values:
- Order lookups need consistency — `0.1`
- Normal support should feel warm but reliable — `0.3`
- Apology emails need a slightly human, less robotic feel — `0.7`
- Book recommendations benefit from variety — `0.9`

Temperature is a property on `HelpBot` with a validator that rejects values outside `0.0–1.0`. It's separate from `Settings` because it changes mid-session.

---

## 10. Putting It All Together — Full Conversation Trace

```
You: Hi, I got a damaged book.
```
- RAG finds "Damaged Items" policy section
- Injected into message as `<policy_context>`
- No tool needed — Claude replies using context + personality

```
You: Order PT-9923, the cover is torn.
```
- RAG finds "Returns" section
- Claude calls `check_order_status("PT-9923")` → tool loop runs
- Claude calls `check_return_eligibility("PT-9923")` → second tool loop
- Claude streams final answer with both results

```
You: return
You: Order PT-9923, torn cover, I'd like a refund, urgent
```
- `extract_return_request()` called with prefill + stop sequence
- Returns structured JSON form
- Bot confirms the filing

```
You: /image photos/cover.jpg
```
- Image read, base64-encoded, sent to Claude
- Damage categorised: "torn cover"
- Finding injected into conversation
- HelpBot acknowledges and asks for order ID

```
You: quit
HelpBot: Thanks for contacting PageTurner. Happy reading!
```
