# HelpBot — Complete Project Walkthrough

**PageTurner Books Customer Support Bot** built with the Claude API.

---

## What This Project Demonstrates

| Claude API Feature | Where Used |
|---|---|
| Multi-turn conversations | `conversation.py` |
| Streaming responses | `output.py` → `stream_reply()` |
| Tool use (function calling) | `tools.py` + `chat.py` |
| Prompt caching | System prompt + tool schemas |
| Prefilling assistant responses | `chat.py` + `main.py` |
| Structured JSON output | `output.py` → `extract_return_request()` |
| Vision (image input) | `media.py` → `ask_about_image()` |
| RAG (retrieval-augmented generation) | `rag.py` |

---

## Project Structure

```
helpbot-project/
├── main.py                          # Entry point — CLI loop
├── pageturner_returns_policy.md     # Source document for RAG
├── requirements.txt
├── .env.example
└── helpbot/
    ├── __init__.py                  # Public exports
    ├── config.py                    # Settings + system prompt
    ├── chat.py                      # HelpBot class — orchestrator
    ├── conversation.py              # Message history manager
    ├── output.py                    # Streaming + structured output
    ├── tools.py                     # Tool schemas + implementations
    ├── rag.py                       # RAG index (vector + BM25)
    └── media.py                     # Image and PDF input
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env from the example
cp .env.example .env

# 3. Add your API keys inside .env
ANTHROPIC_API_KEY=sk-ant-api03-...
VOYAGE_API_KEY=pa-...

# 4. Run
python main.py
```

---

## Architecture — How Everything Connects

```
main.py
  │
  ├─ Settings.from_env()          reads .env keys
  ├─ RAGIndex.build()             embeds policy doc at startup
  └─ HelpBot(settings, rag)
        │
        └─ .chat(user_input)
              │
              ├─ _augment_with_rag()    fetches relevant policy chunks
              ├─ Conversation.add_user()
              └─ _run_turn()
                    │
                    ├─ _call()           sends to Claude (non-streaming)
                    │    └─ tool_use?
                    │         ├─ YES → execute_tool_calls() → loop
                    │         └─ NO  → stream_reply() → done
                    └─ Conversation.add_assistant()
```

---

## File-by-File Walkthrough

---

### `config.py` — Settings & System Prompt

**What it does:** Loads API keys from `.env` and defines the bot's personality.

```python
@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 1000
    temperature: float = 0.3
    voyage_api_key: str = ""
```

`Settings` is a frozen dataclass — immutable after creation. `from_env()` is the only constructor used in production; it reads `ANTHROPIC_API_KEY` and crashes early with a clear message if it's missing.

**The system prompt** (`SYSTEM_PROMPT`) defines HelpBot's character:
- Warm, bookshop-employee personality
- Explicit rule: never fabricate — if unsure, say so
- Step-by-step complaint handling instructions
- A concrete example (few-shot) showing the expected response style
- Instruction to use only `<policy_context>` content for policy questions

The system prompt is marked for **prompt caching** in `chat.py` (see below), so it's only billed once per session.

---

### `conversation.py` — Message History

**What it does:** Manages the full message list that gets sent to Claude on every turn.

```python
@dataclass
class Conversation:
    _messages: list[dict[str, Any]] = field(default_factory=list)
```

The Claude API is **stateless** — it has no memory between calls. Every request must include the complete conversation history. This class is the single source of truth for that history.

Key methods:
| Method | Purpose |
|---|---|
| `add_user(text)` | Adds a user turn |
| `add_assistant(text)` | Adds a plain assistant text turn |
| `add_assistant_raw(content)` | Adds raw content blocks (includes `tool_use` blocks) |
| `add_tool_results(results)` | Adds tool result blocks as a user turn |
| `pop_last()` | Removes the last message (used during prefill flow) |

**Why `add_tool_results` is a user turn:** The Claude API requires tool results to be sent back in a `user` role message. This is a quirk of the API — Claude "speaks" the tool call, you "respond" with the result.

---

### `tools.py` — Tool Definitions & Execution

**What it does:** Defines the 3 tools Claude can call, implements them with mock data, and runs them when Claude requests it.

#### The 3 Tools

**1. `check_order_status(order_id)`**
Looks up shipping/delivery status from a hardcoded `_ORDERS` dict. In production, this would hit a real orders database. Returns status, carrier, and ETA.

**2. `check_return_eligibility(order_id)`**
Calculates how many days since the order was placed and whether it's within the 30-day return window. Uses `date.today()` so it's always current.

**3. `get_estimated_restock_date(book_title)`**
Looks up a book in the `_BOOKS` dict (case-insensitive). Returns whether it's in stock and when it's expected back.

#### Tool Schemas

Each tool has a JSON schema that tells Claude what it does and what parameters it expects:

```python
{
    "name": "check_order_status",
    "description": "Looks up the current shipping and delivery status...",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "PageTurner order ID in the format PT-XXXX"
            }
        },
        "required": ["order_id"]
    }
}
```

The **last tool schema** has `"cache_control": {"type": "ephemeral"}` — this caches the entire tools list so it's not re-billed on every turn.

#### Tool Execution Loop

```python
def execute_tool_calls(blocks):
    for block in blocks:
        if block.type != "tool_use":
            continue
        fn = _REGISTRY.get(block.name)
        output = fn(**block.input)
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": json.dumps(output),
        })
    return results
```

Claude can request multiple tools in one turn. `execute_tool_calls` runs all of them and returns a list of results that get fed back into the conversation.

---

### `chat.py` — The HelpBot Orchestrator

**What it does:** The core class. Owns the client, conversation, and coordinates RAG + tools + streaming.

#### Prompt Caching

```python
_CACHED_SYSTEM = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"},
    }
]
```

The system prompt is wrapped with `cache_control` before being sent to Claude. This means after the first request, Anthropic caches the prompt tokens server-side. Subsequent requests in the same session read from cache — **cache reads cost ~10% of normal input token price**, which adds up significantly in long conversations.

#### RAG Augmentation

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

Before sending any user message to Claude, the bot retrieves the most relevant policy chunks and prepends them in `<policy_context>` tags. The system prompt instructs Claude to use only this context for policy questions — preventing hallucination.

#### The Tool Loop (`_run_turn`)

```python
def _run_turn(self) -> StreamResult:
    while True:
        response = self._call()                          # non-streaming call
        self._conversation.add_assistant_raw(response.content)

        if response.stop_reason != "tool_use":
            # Claude is done with tools — stream the final reply
            self._conversation.pop_last()
            result = stream_reply(...)
            self._conversation.add_assistant(result.text)
            return result

        # Claude wants to call a tool
        tool_results = execute_tool_calls(response.content)
        self._conversation.add_tool_results(tool_results)
        # loop again — Claude will process results and either reply or call more tools
```

**Two-phase approach:**
1. **Non-streaming call** to handle tool use (streaming + tool use don't mix cleanly)
2. **Streaming call** only for the final human-facing reply

This loop handles chained tool calls — Claude can call `check_order_status` and then `check_return_eligibility` in the same turn before giving the final answer.

#### Prefilling

```python
if self._prefill:
    self._conversation.add_assistant(self._prefill)

result = stream_reply(..., prefill=self._prefill)

if self._prefill:
    self._conversation.pop_last()  # remove bare prefill entry
```

Prefilling works by adding a partial assistant message before sending, which forces Claude to continue from that exact phrase. The temporary entry is removed after streaming so the history stays clean, then the full response (prefill + streamed text) is stored.

---

### `output.py` — Streaming & Structured Output

**What it does:** Two distinct output modes — streaming for conversation, JSON extraction for structured data.

#### `stream_reply()` — Token-by-Token Streaming

```python
with client.messages.stream(...) as stream:
    for chunk in stream.text_stream:
        emit(chunk)           # prints to stdout immediately
        streamed_text += chunk

    usage = stream.get_final_message().usage
```

`text_stream` is an iterator that yields text chunks as Claude generates them. The user sees the response appear word-by-word instead of waiting for the full response.

After streaming, `get_final_message()` returns the complete response with token usage stats (including cache hits). These are printed after every response so you can see the caching working in real time.

#### `extract_return_request()` — Structured JSON Output

```python
response = client.messages.create(
    model=model,
    max_tokens=300,
    messages=[
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "```json"},  # prefill forces JSON
    ],
    stop_sequences=["```"],
)
```

This is the **prefill + stop sequence** technique for guaranteed JSON output:
- Prefill `"```json"` forces Claude to start with a JSON block
- Stop sequence `"```"` makes Claude stop exactly when the JSON ends
- Result is always clean, parseable JSON with no markdown wrapper

This is simpler than asking Claude to "respond in JSON" because it physically constrains the output format.

---

### `rag.py` — Retrieval-Augmented Generation

**What it does:** Builds a searchable index of the policy document and retrieves relevant chunks at query time using hybrid search.

#### Step 1: Chunking

```python
def chunk_by_section(text: str) -> list[str]:
    raw = text.split("\n## ")
    ...
```

The policy document is split at every `##` H2 header. Each section (e.g. "Returns", "Shipping", "Damaged Items") becomes its own chunk. This is better than fixed character-length chunking because sections are semantically coherent.

#### Step 2: Embedding (at startup)

```python
client = voyageai.Client(api_key=voyage_api_key)
chunks = chunk_by_section(path.read_text())
embeddings = client.embed(texts=chunks, model="voyage-3").embeddings

for chunk, vector in zip(chunks, embeddings):
    self._vector_store.add(vector, chunk)
self._bm25_store.index(chunks)
```

All chunks are embedded once at startup using Voyage AI's `voyage-3` model and stored in the `VectorStore`. BM25 keyword index is also built from the same chunks.

#### Step 3: Vector Store (cosine similarity)

```python
def search(self, query_vector, top_k=3):
    scores = [
        float(np.dot(q, v) / (q_norm * np.linalg.norm(v) + 1e-10))
        for v in self._vectors
    ]
    top_indices = sorted(..., key=lambda i: scores[i], reverse=True)
    return [self._docs[i] for i in top_indices[:top_k]]
```

Pure numpy — no external vector DB needed. Cosine similarity scores each chunk against the query embedding and returns the top-K most similar ones.

#### Step 4: BM25 Keyword Store

```python
self._bm25 = BM25Okapi([doc.lower().split() for doc in docs])
```

BM25 (Best Match 25) is a classic keyword ranking algorithm — it scores documents by term frequency adjusted for document length. It catches exact keyword matches that semantic search might miss.

#### Step 5: Hybrid Search with Reciprocal Rank Fusion

```python
def search(self, query, voyage_api_key, top_k=2):
    semantic = self._vector_store.search(query_vector, top_k=top_k)
    keyword = self._bm25_store.search(query, top_k=top_k)

    scores: dict[str, float] = {}
    for rank, doc in enumerate(semantic):
        scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)
    for rank, doc in enumerate(keyword):
        scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)

    return sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]
```

**Reciprocal Rank Fusion (RRF):** Combines semantic and keyword results without needing to normalize their scores. A document ranked #1 by semantic search gets score `1/1 = 1.0`. Ranked #2 by keyword search it gets an additional `1/2 = 0.5`. Total: `1.5`. This simple formula consistently outperforms single-method retrieval.

---

### `media.py` — Image & PDF Input

**What it does:** Sends image or PDF files to Claude as base64-encoded content.

```python
def ask_about_image(client, model, image_path, question):
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
                        "data": base64.standard_b64encode(path.read_bytes()).decode()
                    }
                },
                {"type": "text", "text": question}
            ]
        }]
    )
    return response.content[0].text
```

The message content is a **list** containing an image block and a text block. Claude reads both together. Supported formats: JPEG, PNG, WebP, GIF.

In `main.py`, the image analysis result is then injected back into the ongoing conversation so HelpBot can act on it (e.g. acknowledge damage and ask for an order ID).

---

### `main.py` — The CLI Loop

**What it does:** The entry point. Initializes everything and runs the interactive loop.

#### Startup Sequence

```python
settings = Settings.from_env()     # load API keys
rag = RAGIndex()
rag.build(POLICY_PATH, settings.voyage_api_key)  # embed policy doc
bot = HelpBot(settings=settings, rag_index=rag)
```

The RAG index is built once at startup. This is the right trade-off — a small one-time cost so every query benefits from fast retrieval.

#### Temperature Presets

```python
_TEMP_PRESETS = {
    "precise":  (0.1, "order lookups — consistent, factual"),
    "support":  (0.3, "standard support — default"),
    "warm":     (0.7, "apology emails — more human-feeling"),
    "creative": (0.9, "book recommendations — varied & surprising"),
}
```

Temperature controls how deterministic vs. creative Claude's responses are. Lower = more predictable. The presets map use-cases to sensible values:
- `precise` (0.1): You want the same answer every time — order numbers, dates, facts
- `support` (0.3): Default — warm but consistent
- `warm` (0.7): Apology emails where slight variation feels more human
- `creative` (0.9): Book recommendations where variety is a feature

Change temperature mid-session with `/temp warm` or `/temp 0.5`.

#### Commands

| Input | Action |
|---|---|
| Any text | Normal chat turn |
| `return` | Structured return request form (uses prefill + stop sequences) |
| `/image path/to/photo.jpg` | Analyse image with Claude Vision |
| `/temp precise` | Switch temperature preset |
| `/temp 0.7` | Set exact temperature |
| `/prefill I apologize` | Force all responses to start with that phrase |
| `/prefill off` | Clear prefill |
| `quit` / `exit` / `bye` | End session |

---

## Key Claude API Concepts Demonstrated

### 1. Prompt Caching
The system prompt and tool schemas are marked with `cache_control: ephemeral`. After the first request, these are cached server-side. Every subsequent turn reads from cache at ~10% of the normal token cost. The token usage printed after each reply shows `cache_read=` and `cache_write=` so you can see this working.

### 2. Tool Use Flow
```
User message → Claude thinks → Claude calls tool → You run tool → 
You return result → Claude thinks → Claude gives final answer
```
This loop repeats until `stop_reason != "tool_use"`. Claude can chain multiple tool calls before answering.

### 3. Streaming
Final responses are streamed token-by-token using `client.messages.stream()`. Tool-use turns are done non-streaming because mixing streaming with tool call handling adds complexity with little benefit.

### 4. Prefill
Adding a partial `assistant` message before sending forces Claude to continue from that exact text. Used two ways here:
- **Conversation prefill** (`/prefill` command): Makes all replies start with a specific phrase
- **JSON extraction**: Prefilling `"```json"` guarantees JSON output without any prose preamble

### 5. RAG with Hybrid Search
Policy questions are answered from retrieved document chunks, not from Claude's training data. This prevents hallucination of policy details. Hybrid search (semantic + BM25 + RRF) is more robust than semantic-only retrieval.

---

## Try These Scenarios

```
# Order tracking (triggers check_order_status tool)
You: Where is my order PT-9923?

# Return eligibility (triggers check_return_eligibility tool)
You: Can I return order PT-0042?

# Policy question (triggers RAG retrieval)
You: What's your return window?

# Out-of-stock lookup (triggers get_estimated_restock_date tool)
You: When will The Midnight Library be back in stock?

# Structured return form
You: return
You: I want to return order PT-7777, the book had missing pages, urgent

# Image damage report
You: /image /path/to/damaged_book.jpg

# Temperature demo
You: /temp creative
You: Can you recommend a book like Project Hail Mary?
You: /temp precise
You: What is the status of order PT-9923?

# Prefill demo
You: /prefill I sincerely apologize
You: My order arrived three weeks late.
```

---

## Token Usage Reading

After every reply you'll see:
```
[tokens  in=1823  out=142  cache_read=1650  cache_write=0  temp=0.3]
```

- `in`: Total input tokens billed this turn
- `out`: Output tokens generated
- `cache_read`: Tokens read from cache (billed at ~10% rate) — this is where you save money
- `cache_write`: Tokens written to cache (billed at ~125% rate, one-time cost on first turn)
- `temp`: Current temperature setting
