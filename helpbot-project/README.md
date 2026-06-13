# HelpBot — AI Customer Support for PageTurner Books

> A fully-featured AI chatbot built with the Anthropic Claude API.  
> Companion project for the course **"Build Real AI Apps with the Claude API"**.

---

## What it does

HelpBot is an AI-powered customer support agent for PageTurner Books, a fictional online bookstore. It demonstrates every major capability of the Claude API in a single, coherent application:

| Capability | What you see |
|---|---|
| Multi-turn memory | Remembers everything said earlier in the conversation |
| Persona & system prompt | Responds in PageTurner's warm, bookish brand voice |
| Streaming | Replies appear word-by-word in real time |
| Tool use | Looks up live order status, return eligibility, and book restock dates |
| Structured output | Extracts clean JSON return-request forms from free text |
| RAG | Searches PageTurner's policy docs before answering policy questions |
| Prompt caching | Caches the system prompt and tool schemas to reduce latency and cost |
| Image & PDF input | Accepts photos of damaged books or PDF policy documents |
| Runtime temperature control | Switch response style mid-session with `/temp` |
| Response prefilling | Force a fixed opening phrase on every reply with `/prefill` |
| Image damage categorisation | `/image` analyses a photo, categorises damage, and opens a support thread |

---

## Project structure

```
├── main.py                        # CLI entry point
├── requirements.txt
├── .env.example                   # Copy to .env and fill in your keys
├── pageturner_returns_policy.md   # Policy document used for RAG
│
└── helpbot/
    ├── __init__.py                # Public API: HelpBot, Settings, RAGIndex
    ├── config.py                  # Settings dataclass + SYSTEM_PROMPT
    ├── conversation.py            # Conversation class (message history)
    ├── tools.py                   # Tool functions, schemas, executor
    ├── rag.py                     # RAGIndex: VectorStore + BM25 + hybrid search
    ├── output.py                  # Streaming + structured JSON extraction
    ├── media.py                   # Image and PDF input helpers
    └── chat.py                    # HelpBot class — orchestrates everything
```

---

## Quickstart

### 1. Clone and install

```bash
git clone <your-repo-url>
cd helpbot
pip install -r requirements.txt
```

### 2. Set up API keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
VOYAGE_API_KEY=...          # Optional — enables RAG. Get one at voyageai.com
```

> **ANTHROPIC_API_KEY** is required. Get yours at [console.anthropic.com](https://console.anthropic.com).  
> **VOYAGE_API_KEY** is optional. Without it, HelpBot still works — RAG is simply disabled.

### 3. Run

```bash
python main.py
```

---

## Usage

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

### Chat commands

| Input | What it does |
|---|---|
| Any message | Normal chat turn — RAG + tools + streaming |
| `return` | Opens the structured return-request flow (outputs JSON form) |
| `quit` / `exit` / `bye` | Ends the session |

### Slash commands

| Command | Example | Effect |
|---|---|---|
| `/temp <value>` | `/temp 0.7` | Set temperature to any float 0.0–1.0 |
| `/temp <preset>` | `/temp creative` | Apply a named preset (see table below) |
| `/temp` | `/temp` | Show the current temperature |
| `/prefill <phrase>` | `/prefill Great news —` | Every reply starts with that phrase |
| `/prefill off` | `/prefill off` | Clear the prefill |
| `/image <path>` | `/image photos/cover.jpg` | Analyse a damaged-book photo and open a support thread |

### Temperature presets

| Preset | Value | Best for |
|---|---|---|
| `precise` | 0.1 | Order lookups — consistent, factual |
| `support` | 0.3 | Standard support — **default** |
| `warm` | 0.7 | Apology emails — more human-feeling |
| `creative` | 0.9 | Book recommendations — varied & surprising |

### Available order IDs for testing

| Order ID | Status | Return eligible? |
|---|---|---|
| `PT-9923` | Shipped — FedEx, arriving tomorrow | Yes (ordered 2026-05-20) |
| `PT-0042` | Processing — ships in 2 business days | Yes (ordered 2026-06-10) |
| `PT-7777` | Delivered — UPS | No (ordered 2026-05-01, outside 30-day window) |

### Available book titles for restock testing

| Title | Status |
|---|---|
| `The Midnight Library` | Out of stock — expected 2026-07-05 |
| `Atomic Habits` | In stock |
| `Project Hail Mary` | Out of stock — expected 2026-06-28 |
| `The Thursday Murder Club` | Out of stock — expected 2026-07-15 |
| `Lessons in Chemistry` | In stock |

---

## Example session

```
You: Where is my order PT-9923?
HelpBot: Let me check that for you... Your order PT-9923 is currently shipped
         via FedEx and is due to arrive tomorrow by 8 pm.

You: Can I still return it?
HelpBot: Good news — PT-9923 was placed on 2026-05-20, so you have plenty of
         time left in your 30-day return window.

You: When will Project Hail Mary be back in stock?
HelpBot: Project Hail Mary is currently out of stock but is expected back
         around 2026-06-28. I can note your interest if you'd like!

You: /temp creative
  [temperature → 0.9  (book recommendations — varied & surprising)]

You: Can you suggest a book for someone who loves mysteries?

You: /prefill Great news — I can help with that!
  [prefill set → "Great news — I can help with that!"]

You: /image photos/damaged_cover.jpg
[Analysing image: damaged_cover.jpg]

HelpBot (image analysis):
Category: torn cover
Description: The front cover has a large tear running diagonally across the spine.

Great news — I can help with that! I'm so sorry your book arrived damaged —
that's not the experience you deserved. Could you share your order number
so I can arrange a replacement or refund, whichever you prefer?

You: return
[Return Request]
Describe your return — include order ID, reason, and urgency:
You: Order PT-9923, torn cover, urgent

--- Return Request Filed ---
{
  "order_id": "PT-9923",
  "reason": "torn cover",
  "urgency": "high",
  "customer_name": null,
  "preferred_resolution": "unknown"
}
----------------------------
```

---

## Architecture

```
User input
    │
    ▼
RAG search ──────────────────────────────────┐
(hybrid: Voyage embeddings + BM25 via RRF)    │
                                              ▼
                                   Augmented user message
                                              │
                                              ▼
                                    Claude API (with tools)
                                              │
                            ┌─────────────────┴──────────────────┐
                            │ tool_use?                           │ end_turn?
                            ▼                                     ▼
                    execute_tool_calls()             [inject prefill if set]
                            │                                     │
                            └──────────► loop          stream_reply() → stdout
                                                                  │
                                                    Conversation history updated
```

**Key design decisions:**

- **`HelpBot` is a class, not a bag of functions.** One instance per session owns the conversation history and all dependencies — including mutable `temperature` and `prefill` that can change mid-session.
- **`Settings` is a frozen dataclass.** Validated at startup via `Settings.from_env()`. Mutable session state (`temperature`, `prefill`) lives on `HelpBot`, not on `Settings`.
- **`RAGIndex` encapsulates both stores.** `VectorStore` (cosine similarity) and `BM25Store` (keyword) are fused at query time via Reciprocal Rank Fusion (RRF).
- **Streaming and the tool loop are separated.** Intermediate tool turns use non-streaming calls for simplicity. Only the final text reply is streamed.
- **Prefill is injected at the API boundary.** A partial assistant message is added to history just before the streaming call so Claude continues from the phrase. It is printed before the stream starts and the stitched text (`prefill + streamed`) is stored in history.
- **`stream_reply` accepts an `on_token` callback.** Defaults to `print`, but callers can redirect output anywhere (WebSocket, queue, file).

---

## Module map

Each file corresponds directly to a course module:

| Module | Topic | File |
|---|---|---|
| 1 | First API call, response parsing, token usage | `config.py` |
| 2 | Multi-turn memory, system prompt, temperature control | `conversation.py`, `config.py`, `chat.py` |
| 3 | Streaming, prefilling, stop sequences, JSON output | `output.py`, `chat.py` |
| 4 | Tool use, multi-turn tool loop, error handling | `tools.py`, `chat.py` |
| 5 | Prompt caching, prompt evaluation | `config.py`, `chat.py` |
| 6 | Chunking, embeddings, vector search, BM25, hybrid RRF | `rag.py` |
| 7 | PDF/image input, image damage categorisation, full assembly | `media.py`, `main.py` |

---

## Tools reference

HelpBot exposes three tools to Claude:

| Tool | Trigger phrase | Returns |
|---|---|---|
| `check_order_status` | "Where is my order?" / "Has it shipped?" | Status, carrier, ETA |
| `check_return_eligibility` | "Can I return order X?" / "How many days do I have?" | Eligible, days remaining |
| `get_estimated_restock_date` | "When will X be back?" / "Is X available?" | In-stock flag, restock date |

---

## Extending HelpBot

### Add a new tool

1. Write the Python function in `helpbot/tools.py`
2. Add its schema to `TOOL_SCHEMAS` (put `cache_control: ephemeral` on the last entry)
3. Register it in `_REGISTRY`

```python
# helpbot/tools.py

def check_gift_card_balance(card_number: str) -> dict:
    # hit your real gift card API here
    return {"card_number": card_number, "balance_usd": 25.00}

_REGISTRY["check_gift_card_balance"] = check_gift_card_balance

# Add to TOOL_SCHEMAS list, moving cache_control to this new last entry
```

### Add a new policy document

Drop any `.md` file into the project and pass its path to `RAGIndex.build()`:

```python
rag = RAGIndex()
rag.build("shipping_faq.md", settings.voyage_api_key)
```

### Use HelpBot as a library

```python
from helpbot import HelpBot, RAGIndex, Settings

settings = Settings.from_env()
rag = RAGIndex()
rag.build("pageturner_returns_policy.md", settings.voyage_api_key)

bot = HelpBot(settings=settings, rag_index=rag)

# Optional: tune for the task
bot.temperature = 0.9          # creative recommendations
bot.prefill = "Great news — "  # forced opener

result = bot.chat("Can you suggest a mystery novel?")
print(result.text)
print(f"Tokens used: {result.input_tokens + result.output_tokens}")
print(f"Cache read:  {result.cache_read_tokens}")
```

---

## Requirements

- Python 3.11+
- `anthropic` — Claude API SDK
- `python-dotenv` — environment variable loading
- `numpy` — cosine similarity in the vector store
- `rank-bm25` — keyword search
- `voyageai` — embedding model for semantic search *(optional)*

---

## License

MIT
