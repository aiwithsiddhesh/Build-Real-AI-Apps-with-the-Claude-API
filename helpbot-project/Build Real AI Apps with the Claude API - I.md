# Build Real AI Apps with the Claude API
## A Beginner's Project-Based Course

> **Course Format:** Self-paced | **Estimated Duration:** 16–18 hours | **Skill Level:** Beginner (basic Python required)

---

## The Single Project: HelpBot for PageTurner Books

Throughout this entire course, you will build **one real app**: **HelpBot** — an AI-powered customer support chatbot for a fictional online bookstore called **PageTurner Books**.

Every concept you learn gets applied directly to HelpBot. By the time you finish the final module, you'll have a fully working chatbot that can:

- Answer customer questions in PageTurner's voice
- Remember what a customer said earlier in the conversation
- Look up real-time order status using tools
- Stream its responses word-by-word for a better experience
- Search PageTurner's policy documents to answer complex questions
- Output structured data like return request forms in clean JSON

You're not learning concepts in isolation. You're building something real, one layer at a time.

---

## Learner Persona

**Name:** Alex — The Curious Builder

**Who they are:** A Python beginner who has completed a basic Python course or worked through tutorials. They understand variables, functions, loops, and maybe a little about calling APIs. They're not a professional developer — they might be a student, a career switcher, a product manager who wants to build something, or someone who simply got excited by AI and wants to understand how it actually works under the hood.

**What they know coming in:**
- Basic Python syntax (functions, dictionaries, lists, loops)
- Some exposure to the concept of APIs (knows what a request is, roughly)
- No prior experience with LLMs, embeddings, or tool use

**What they want:**
- To stop feeling like AI is a black box
- To build a real, working AI app they can show people
- To understand the actual mechanics — not just copy-paste code from Stack Overflow

**The gap:**
- They know Python but have never called an LLM API
- They don't know how to structure AI conversations in code
- They have no idea what tool use, RAG, or embeddings are

**Time available:** ~3–4 hours per week, flexible schedule

**Format:** Fully self-paced, video + written notes + coding exercises

**Success looks like:** By the end, Alex can open a blank Python file and build a multi-turn AI chatbot with tool use and document search — from memory and intuition, not just copying code.

---

## Course-Level Learning Outcomes

By the end of this course, learners will be able to:

1. **Call** the Anthropic Claude API from Python and interpret every part of the response
2. **Build** multi-turn conversations that maintain context across multiple exchanges
3. **Write** system prompts that reliably shape Claude's tone, persona, and behavior
4. **Implement** response streaming to create real-time AI experiences in applications
5. **Create** tool-enabled chatbots that fetch live data and perform actions outside Claude's training knowledge
6. **Generate** clean, structured JSON output from Claude without any extra formatting noise
7. **Build** a basic RAG pipeline that chunks documents, embeds them, and retrieves relevant context for Claude's answers

---

## Module Map

| # | Module Title | Key Outcomes Covered | Project Milestone | Est. Time |
|---|--------------|---------------------|-------------------|-----------|
| 1 | Getting Started: Your First AI Call | 1 | HelpBot answers its first question | 2 hrs |
| 2 | Real Conversations: Memory & Persona | 2, 3 | HelpBot remembers customers + has a personality | 3 hrs |
| 3 | Better UX: Streaming & Output Control | 4, 6 | HelpBot streams and returns clean JSON tickets | 2.5 hrs |
| 4 | Superpowers: Tool Use | 5 | HelpBot checks live order status | 3 hrs |
| 5 | Smarter Prompts & Speed | 1, 3 | HelpBot responds faster and more accurately | 2 hrs |
| 6 | HelpBot Learns from Documents (RAG) | 7 | HelpBot searches PageTurner's policy docs | 3.5 hrs |
| 7 | Finishing HelpBot & Going Further | All | Complete, working HelpBot deployed | 2 hrs |

**Total: ~18 hours**

---

---

# MODULE 1: Getting Started — Your First AI Call

**Module outcomes:** Learners will be able to call the Claude API from Python and interpret every part of the response.

**Total time:** ~2 hours

---

## Lesson 1.1 — How Claude Actually Thinks (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook
Before we write a single line of code, let's answer a question that most beginner tutorials completely skip: *What's actually happening when you send a message to Claude?*

Most people imagine there's some kind of giant search engine on the other side. There isn't. Claude isn't looking anything up. It's doing something much stranger — and once you understand it, you'll write dramatically better prompts.

### Core Content

**The Three Claude Families**

Anthropic currently ships three flavours of Claude, each built for a different job:

- **Claude Haiku** — The speedster. Lowest cost, fastest response. Great for tasks where you need answers in milliseconds and can tolerate slightly less nuance. Think live chat suggestions or real-time autocomplete.

- **Claude Sonnet** — The workhorse. Strong intelligence, reasonable cost, solid speed. This is where most real applications live, including what we'll use for HelpBot.

- **Claude Opus** — The heavyweight. Highest intelligence, handles complex multi-step reasoning and planning beautifully. Costs more, takes longer. You'd use this when a task genuinely needs depth — like evaluating a legal contract or generating a strategic plan.

For most projects, including ours, **Sonnet is the right choice.** It's fast enough for real users, smart enough for real tasks, and won't burn through credits.

**What happens inside Claude's brain (simplified)**

When you send a message, here's what happens in rough terms:

1. **Tokenisation** — Your text gets broken into *tokens*. Not words exactly — more like syllables or word-chunks. "PageTurner" might be two tokens. A space before "the" is its own token. This matters because you get charged per token and there's a max limit per request.

2. **Embedding** — Each token becomes a long list of numbers. These numbers represent meaning. Words with similar meanings end up with similar numbers. This is how Claude knows "unhappy" and "disappointed" are related without being told.

3. **Contextualisation** — The model looks at all the tokens together and adjusts each word's meaning based on its neighbours. "Bank" next to "river" means something different than "bank" next to "account".

4. **Generation** — The model predicts what token should come next, picks one based on probability (with some controlled randomness), adds it, and repeats until done.

That's it. One token at a time. There's no database being searched. No facts being looked up. Just very sophisticated autocomplete — which is why knowing what you want to tell it matters so much.

**Stop reason and max_tokens**

Two important parameters:
- **max_tokens** — You set a hard limit on how long Claude's response can be. It's a safety net, not a target. If Claude finishes naturally before hitting the limit, it stops.
- **stop_reason** — The API tells you why Claude stopped: `"end_turn"` (finished naturally) or `"max_tokens"` (hit the limit — response may be cut off).

### Practice Activity
**Reflection prompt (3 min):** Before moving on, predict: if you asked Claude "What's the capital of France?" — how many tokens do you think the *answer* would be? What about the question itself? (We'll verify this in the next lesson.)

### Wrap-Up
You now know that Claude is a token-prediction machine, not a search engine. There are three model sizes with real trade-offs. In the next lesson, we set up your environment and make your very first real API call.

---

## Lesson 1.2 — Setting Up Your Environment (Demo)
**Type:** Demo | **Duration:** 25 min

### Hook
Every project has a boring-but-necessary setup step. Let's get through it quickly and get to the fun part.

### Core Content

**What we're installing**

```bash
pip install anthropic python-dotenv
```

- `anthropic` — The official Python SDK for the Claude API. Handles all the HTTP plumbing for you.
- `python-dotenv` — Lets you store your API key in a file instead of hard-coding it. This is a real security habit worth building early.

**Your API key**

Sign up at `console.anthropic.com`, navigate to API Keys, and generate a key. Treat it like a password. Never put it directly in your code.

Instead, create a file called `.env` in your project folder:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

Then add `.env` to your `.gitignore` so it never accidentally ends up on GitHub.

**Loading the key in Python**

```python
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()  # Reads .env file and loads variables into environment

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"
```

That `client` object is your connection to Claude. Everything we do in this course runs through it.

### Practice Activity
**Guided exercise:** Set up your project folder, install packages, create the `.env` file, and run a quick sanity check — just `print(client)` to confirm your setup works without errors.

---

## Lesson 1.3 — HelpBot's First Words (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Hook
This is the moment. Three lines of Python, and you'll have a real AI answering a real question on PageTurner's behalf.

### Core Content

**The basic API call**

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=500,
    messages=[
        {"role": "user", "content": "What are PageTurner's store hours?"}
    ]
)

print(response.content[0].text)
```

Let's unpack every argument:

- `model` — Which Claude version to use
- `max_tokens` — The response length ceiling
- `messages` — A list of conversation turns. Each turn has a `role` (`"user"` or `"assistant"`) and `content` (the text)

**Reading the full response object**

The response is more than just text. Print `response` directly and you'll see:

```python
print(response)
# Message(
#   id='msg_abc123',
#   content=[TextBlock(text="PageTurner's store hours are...", type='text')],
#   model='claude-sonnet-4-6',
#   stop_reason='end_turn',
#   usage=Usage(input_tokens=14, output_tokens=47)
# )
```

Key fields to know:
- `response.content[0].text` — The actual reply text
- `response.stop_reason` — Why Claude stopped (`end_turn` = natural finish)
- `response.usage.input_tokens` — How many tokens your question used
- `response.usage.output_tokens` — How many tokens the reply used

**Project application — first HelpBot function**

```python
def ask_helpbot(question: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# Test it
print(ask_helpbot("Do you sell used books?"))
```

### Practice Activity
**Guided exercise:** Call `ask_helpbot` with 3 different customer questions. Then also `print(response.usage.input_tokens + response.usage.output_tokens)` to see how many total tokens each question used. Does a longer question use more input tokens?

### Wrap-Up
You've made your first real AI API call. HelpBot can answer questions — but it doesn't know it's supposed to be a bookstore assistant, and it forgets everything between messages. We fix both of those in Module 2.

---

## Lesson 1.4 — Understanding Tokens & Costs (Concept)
**Type:** Concept | **Duration:** 15 min

### Core Content

**Why tokens matter**
Anthropic charges per token — both input (what you send) and output (what Claude replies). Keeping prompts focused and capping max_tokens appropriately is a real skill that saves money at scale.

A rough rule of thumb: 1 token ≈ 0.75 English words. So a 100-word message ≈ ~130 tokens.

**Practical implications for HelpBot**

If a customer's full conversation history gets sent with every message (which we'll do in Module 2), a long conversation will use a lot of input tokens. That's fine for a prototype — but in production, you'd want strategies like summarising old messages.

### Practice Activity
**Mini-quiz (5 questions):** Cover token estimation, stop reasons, and model selection decisions.

---

## Module 1 Project Checkpoint ✅

At the end of Module 1, your HelpBot can:
- Accept a customer's question as a string
- Send it to Claude via the API
- Return Claude's text response

**Limitation:** It has no memory, no personality, and no idea it works for a bookstore. That's next.

---

---

# MODULE 2: Real Conversations — Memory & Persona

**Module outcomes:** Build multi-turn conversations; write system prompts that shape Claude's behavior.

**Total time:** ~3 hours

---

## Lesson 2.1 — The Memory Problem (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook
Try this: ask HelpBot "What's your name?" and then immediately ask "What did I just ask you?" Watch what happens. Claude has no idea what you just said. Every API call is completely independent — a clean slate. This is the default behaviour, and it's a problem for any real chatbot.

### Core Content

**Why the API has no memory**

The Anthropic API doesn't store your conversation history anywhere. When you make a request, Claude sees exactly what you send — nothing more, nothing less. No session. No cookies. No server-side memory.

This is actually a feature, not a bug. It keeps the API stateless, fast, and scalable. But it means *you* are responsible for maintaining the conversation history on your end.

**The solution: send the whole history every time**

The messages parameter is a list. Instead of always sending a single message, you'll build up a list and send the full conversation with every new request:

```python
messages = [
    {"role": "user", "content": "I need to return a book"},
    {"role": "assistant", "content": "Of course! I can help with that..."},
    {"role": "user", "content": "The order number is 12345"}
]
```

Claude reads the whole list, understands the context, and replies appropriately.

### Practice Activity
**Reflection prompt:** Write out (in plain English, no code) what the `messages` list would look like after a 3-turn conversation between a customer asking about a damaged book delivery. Practice thinking in terms of roles and content before writing any code.

---

## Lesson 2.2 — Building HelpBot's Memory (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

**Helper functions for managing history**

```python
def add_user_message(messages: list, text: str) -> list:
    messages.append({"role": "user", "content": text})
    return messages

def add_assistant_message(messages: list, text: str) -> list:
    messages.append({"role": "assistant", "content": text})
    return messages
```

**The updated chat function**

```python
def chat(messages: list) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=messages
    )
    reply_text = response.content[0].text
    add_assistant_message(messages, reply_text)  # Store Claude's reply
    return reply_text
```

**A full conversation loop**

```python
conversation = []

# Turn 1
add_user_message(conversation, "Hi, I ordered a book three weeks ago and it hasn't arrived.")
reply = chat(conversation)
print("HelpBot:", reply)

# Turn 2
add_user_message(conversation, "My order number is PT-9923.")
reply = chat(conversation)
print("HelpBot:", reply)

# Turn 3 — does it remember?
add_user_message(conversation, "What was my order number again?")
reply = chat(conversation)
print("HelpBot:", reply)  # It should remember PT-9923!
```

### Practice Activity
**Guided exercise:** Run the above. Then extend the conversation to 5 turns. Try asking Claude in turn 5 to summarise the entire conversation — it should be able to, because the full history is in the messages list.

---

## Lesson 2.3 — Giving HelpBot a Personality (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Hook
Right now, HelpBot sounds like a generic AI assistant. But PageTurner Books has a brand voice — warm, bookish, slightly witty, always helpful. System prompts are how we bake that personality in permanently.

### Core Content

**What a system prompt is**

A system prompt is a special instruction you pass alongside the conversation. It's not from the user — it comes from *you*, the developer, and it sets the rules Claude follows throughout the conversation.

```python
SYSTEM_PROMPT = """
You are HelpBot, the friendly customer support assistant for PageTurner Books — 
an independent online bookstore that loves great stories and great service.

Your personality:
- Warm and approachable, like a knowledgeable bookshop employee
- You occasionally use gentle book-related metaphors ("Let's get to the final chapter 
  of this issue...")
- You never make up information you don't have — if you don't know, say so honestly
- You always try to resolve the customer's issue or escalate clearly

You can help with: order tracking, returns, account issues, and general bookstore questions.
You cannot: process payments or access real databases (yet).

Always greet the customer by name if they share it.
"""
```

**Passing the system prompt**

```python
def chat(messages: list, system: str = None) -> str:
    params = {
        "model": MODEL,
        "max_tokens": 500,
        "messages": messages
    }
    if system:
        params["system"] = system  # System prompt is a top-level parameter, not a message
    
    response = client.messages.create(**params)
    reply_text = response.content[0].text
    add_assistant_message(messages, reply_text)
    return reply_text
```

**Key principle:** The system prompt guides *how* Claude responds, not *what* the user asked. The same question gets treated very differently with and without it.

### Practice Activity
**Guided exercise:** Run the same 3-turn conversation from Lesson 2.2, once without the system prompt and once with it. Notice the difference in tone, language, and the bookstore-specific personality. Write down 3 specific differences.

---

## Lesson 2.4 — Controlling Creativity with Temperature (Concept + Practice)
**Type:** Concept + Practice | **Duration:** 25 min

### Core Content

**What temperature actually does**

Temperature is a number between 0 and 1 that controls how "random" Claude's token selection is.

At temperature 0, Claude always picks the single most likely next token. The output is deterministic — ask the same question twice, get the same answer.

At higher temperatures (0.7, 0.9, 1.0), Claude gives more probability to less-likely tokens. This creates variation, creativity, and sometimes unexpected — but interesting — results.

**When to use what:**

| Task | Temperature | Why |
|------|------------|-----|
| Checking order status | 0.0 – 0.2 | Needs consistent, accurate responses |
| Standard customer support | 0.3 – 0.5 | Slight variation, but professional |
| Writing personalised apology emails | 0.7 – 0.9 | Want unique, human-feeling language |
| Brainstorming book recommendations | 0.8 – 1.0 | Variety and surprise is the point |

**For HelpBot:** Most responses should be at 0.3 — consistent but not robotic.

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=500,
    messages=messages,
    system=SYSTEM_PROMPT,
    temperature=0.3  # Add this parameter
)
```

### Practice Activity
**Experiment:** Ask HelpBot "Can you suggest a book for someone who loves mystery novels?" with temperature=0, then temperature=0.9. Run each version 3 times. Compare the variety (or lack of it) in the recommendations.

---

## Module 2 Project Checkpoint ✅

HelpBot can now:
- Remember everything a customer said in this conversation
- Speak in PageTurner's warm, bookish voice
- Adjust creativity level based on task type

**What's missing:** Customers stare at a blank screen for 10-20 seconds waiting for a response. That's terrible UX. We fix it in Module 3 with streaming.

---

---

# MODULE 3: Better UX — Streaming & Output Control

**Module outcomes:** Implement streaming; generate clean structured JSON output.

**Total time:** ~2.5 hours

---

## Lesson 3.1 — The 10-Second Problem (Concept)
**Type:** Concept | **Duration:** 15 min

### Hook
Open any modern AI chat app — ChatGPT, Claude.ai, Gemini. Notice how the text appears word-by-word as it's being written? That's streaming. Without it, users wait in silence for potentially 10-30 seconds before seeing anything. That wait feels broken, even if it's technically working.

### Core Content

**How streaming works**

Instead of waiting for Claude to finish generating the entire response and then sending it all at once, streaming sends the response in small chunks as each piece is generated.

These chunks arrive as a stream of *events*. The most important event type is `content_block_delta` — each one contains a small piece of text (sometimes just a single word or even part of a word).

Your job is to listen for these events and forward each chunk to the user as it arrives.

**The types of events**

When streaming, you'll see these events in sequence:
- `message_start` — Claude acknowledged your request, about to start
- `content_block_start` — The text generation begins
- `content_block_delta` — A text chunk arrives (this is the main one you care about)
- `content_block_stop` / `message_stop` — Generation is complete

---

## Lesson 3.2 — Implementing Streaming in HelpBot (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Core Content

**Option 1 — Full manual event handling**

```python
with client.messages.stream(
    model=MODEL,
    max_tokens=500,
    messages=messages,
    system=SYSTEM_PROMPT,
) as stream:
    for text_chunk in stream.text_stream:
        print(text_chunk, end="", flush=True)  # Print each chunk as it arrives
    print()  # New line after response finishes

# Get the full assembled message for storing in history
final_message = stream.get_final_message()
full_reply = final_message.content[0].text
```

**Key detail:** `stream.text_stream` is a convenience property that automatically extracts just the text from `content_block_delta` events. You don't have to parse events manually.

**Storing streamed responses**

The streamed reply still needs to go into your conversation history. Use `stream.get_final_message()` to get the fully assembled message after streaming finishes.

```python
def chat_streaming(messages: list, system: str = None) -> str:
    params = {
        "model": MODEL,
        "max_tokens": 500,
        "messages": messages,
        "temperature": 0.3
    }
    if system:
        params["system"] = system

    full_reply = ""
    with client.messages.stream(**params) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
            full_reply += chunk
    print()
    
    add_assistant_message(messages, full_reply)
    return full_reply
```

### Practice Activity
**Guided exercise:** Replace your old `chat()` function with `chat_streaming()` and re-run your 3-turn conversation. Notice how responses now appear progressively. Then test with a longer question (e.g. "Can you give me a 5-step guide to tracking my PageTurner order?") to really see the difference.

---

## Lesson 3.3 — Output Control: Prefilling & Stop Sequences (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 25 min

### Hook
Two useful tricks that give you precise control over Claude's responses — without writing a longer prompt.

### Core Content

**Prefilling: steering Claude's response direction**

You can add a partial assistant message at the end of the conversation. Claude treats it as something it already started saying, and continues from that exact point.

```python
messages = [
    {"role": "user", "content": "Which is better for a long trip: audiobooks or ebooks?"},
    {"role": "assistant", "content": "For long trips, ebooks are the better choice because"}
    #                                  ↑ Claude continues from here, making the case for ebooks
]
```

This is especially useful when you need to guarantee Claude opens with a specific phrase or structure.

**Important:** When you read the response, it won't include the prefill text. You need to stitch them together yourself: `prefill_text + response.content[0].text`.

**Stop sequences: ending Claude mid-generation**

Sometimes you want Claude to stop when it hits a specific word or phrase — even if it hasn't finished a natural sentence.

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=200,
    messages=[{"role": "user", "content": "List the steps to return a book, numbered 1 to 5."}],
    stop_sequences=["4."]  # Claude stops the moment it generates "4."
)
```

This is useful when you need to limit output length in a specific way — like stopping a list after 3 items, or stopping a poem after one stanza.

### Practice Activity
**Guided exercise:** Use prefilling to make HelpBot always start its responses with "Great news — I can help with that!" and see how it affects the rest of the reply.

---

## Lesson 3.4 — Clean JSON Output from HelpBot (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Hook
When a customer requests a return, we don't just want Claude to *write about* the return — we want structured data we can process programmatically: an order number, a reason, a timestamp. That means JSON. The challenge: Claude naturally wraps everything in explanatory text and markdown. We need to strip that away.

### Core Content

**The structured output pattern**

Combine prefilling + stop sequences to extract raw JSON every time:

```python
def get_structured_return_request(customer_message: str) -> dict:
    messages = [
        {
            "role": "user",
            "content": f"""
Extract a return request from this customer message.
Return ONLY a JSON object with these fields: order_id, reason, urgency (low/medium/high).

Customer message: {customer_message}
"""
        },
        {
            "role": "assistant",
            "content": "```json"  # Prefill — Claude continues from here
        }
    ]
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=messages,
        stop_sequences=["```"]  # Stop when the closing fence appears
    )
    
    raw_json = "```json" + response.content[0].text  # Stitch prefill + response
    # Extract just the JSON part
    json_str = raw_json.replace("```json", "").replace("```", "").strip()
    return json.loads(json_str)

# Test
result = get_structured_return_request(
    "Hi, I need to return order PT-9923. The book arrived with a torn cover. It's urgent."
)
print(result)
# {'order_id': 'PT-9923', 'reason': 'damaged goods - torn cover', 'urgency': 'high'}
```

### Practice Activity
**Guided exercise:** Extend the return request schema to also capture `customer_name` if mentioned, and `preferred_resolution` (refund/exchange/store credit). Test with 5 different customer messages including edge cases like "I just don't like the book."

---

## Module 3 Project Checkpoint ✅

HelpBot now:
- Streams responses word-by-word for a great user experience
- Can extract structured JSON from unstructured customer messages
- Gives you control over response direction with prefilling

**What's missing:** HelpBot can't actually *check* anything. It can't look up real order status, it can't check shipping, it can't set a callback. It's all talk. Tools are next.

---

---

# MODULE 4: Superpowers — Tool Use

**Module outcomes:** Create tools that Claude can call; handle multi-tool conversations in a loop.

**Total time:** ~3 hours

---

## Lesson 4.1 — Why Claude Needs Tools (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook
Claude's training data has a cutoff date. It doesn't know what happened yesterday. It definitely doesn't know what's in PageTurner's order database. But a customer asking "Where's my order?" doesn't care about that — they want an answer.

Tools are the bridge between Claude's language capabilities and the real world.

### Core Content

**The tool use flow — 5 steps**

1. **You tell Claude what tools exist** — by describing them in your API request
2. **Claude decides it needs a tool** — it replies with a special "tool use" block instead of text
3. **Your code runs the actual tool** — fetches the data, calls the API, whatever the tool does
4. **You send the result back to Claude** — as a follow-up message
5. **Claude generates the final response** — now informed by real data

Claude never directly calls external APIs. It just *describes* what it wants, and your code does the actual work. This design is intentional — it means you stay in control of what actually happens.

---

## Lesson 4.2 — Your First Tool: Order Status Checker (Demo)
**Type:** Demo | **Duration:** 35 min

### Core Content

**Step 1: Write the Python function**

```python
import json
from datetime import datetime, timedelta
import random

def check_order_status(order_id: str) -> dict:
    """
    Looks up an order's status. In a real app, this hits your database.
    For now, we're simulating with fake data.
    """
    if not order_id or not order_id.startswith("PT-"):
        raise ValueError(f"Invalid order ID format: '{order_id}'. Must start with 'PT-'.")
    
    # Fake order database
    fake_orders = {
        "PT-9923": {"status": "shipped", "carrier": "FedEx", "eta": "Tomorrow by 8pm"},
        "PT-0042": {"status": "processing", "carrier": None, "eta": "Ships in 2 business days"},
        "PT-7777": {"status": "delivered", "carrier": "UPS", "eta": "Delivered yesterday"},
    }
    
    if order_id in fake_orders:
        return fake_orders[order_id]
    else:
        return {"status": "not_found", "message": "Order not found in system."}
```

**Step 2: Write the tool schema**

The schema tells Claude what the function does, what arguments it needs, and when to use it. This is written in JSON Schema format:

```python
check_order_status_schema = {
    "name": "check_order_status",
    "description": """
        Looks up the real-time shipping and delivery status of a PageTurner order.
        Use this whenever a customer asks about where their order is, when it will arrive,
        or whether it has been delivered. Returns current status, carrier, and estimated 
        delivery date.
    """,
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The customer's PageTurner order ID, formatted as 'PT-XXXX' (e.g. PT-9923)"
            }
        },
        "required": ["order_id"]
    }
}

TOOLS = [check_order_status_schema]
```

---

## Lesson 4.3 — Handling Tool Calls in Code (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

**What Claude's response looks like when it wants to use a tool**

```python
# Normal text response — content has one TextBlock
response.content = [TextBlock(text="Hello! How can I help you?", type='text')]

# Tool use response — content has a ToolUseBlock
response.content = [
    TextBlock(text="Let me check that for you...", type='text'),
    ToolUseBlock(
        id='toolu_abc123',            # Unique ID for this specific tool call
        input={'order_id': 'PT-9923'}, # Arguments Claude wants to pass
        name='check_order_status',     # Which tool to call
        type='tool_use'
    )
]
```

**Sending the tool result back**

```python
def send_tool_result(messages: list, tool_use_id: str, result: dict) -> None:
    """Adds a tool result message to the conversation history."""
    messages.append({
        "role": "user",  # Tool results go in a user message
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use_id,  # Must match the ToolUseBlock ID
            "content": json.dumps(result)  # Convert dict to string
        }]
    })
```

**Why `tool_use_id` matters:** If Claude requests multiple tools in one message, each gets a unique ID. The IDs link each result to the right request so Claude knows which result answers which question.

### Practice Activity
**Guided exercise:** Add the tools parameter to your `chat()` function and test with: "Where is my order PT-9923?" — Step through the flow manually: print the first response to see the tool use block, then call the function, then send the result, then print the final response.

---

## Lesson 4.4 — Multi-Turn Tool Conversations (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

**The problem with one round**

Claude can request multiple tools in a single conversation. Worse, you can't predict *how many* tools a given question will require. A customer saying "Check my order and tell me if I can still return it" might trigger 2 tool calls sequentially.

**The solution: a while loop**

```python
def run_tool(tool_name: str, tool_input: dict):
    """Routes tool calls to the right function."""
    if tool_name == "check_order_status":
        return check_order_status(tool_input["order_id"])
    # Add more tools here as we build them
    raise ValueError(f"Unknown tool: {tool_name}")

def process_tool_calls(message_content: list) -> list:
    """Finds all tool use blocks and executes them, returning results."""
    tool_results = []
    for block in message_content:
        if block.type == "tool_use":
            try:
                result = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                    "is_error": False
                })
            except Exception as e:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(e),
                    "is_error": True  # Claude will know the tool failed
                })
    return tool_results

def run_conversation(user_input: str) -> str:
    """Runs a full conversation turn, handling any number of tool calls."""
    messages = []
    add_user_message(messages, user_input)
    
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=TOOLS,
            temperature=0.3
        )
        
        # Append Claude's response to history (including any tool use blocks)
        messages.append({"role": "assistant", "content": response.content})
        
        # If Claude is done requesting tools, return the final text
        if response.stop_reason != "tool_use":
            return " ".join(
                block.text for block in response.content 
                if hasattr(block, "text")
            )
        
        # Otherwise, execute the tool calls and send results back
        tool_results = process_tool_calls(response.content)
        messages.append({"role": "user", "content": tool_results})
        # Loop continues...

# Test it
print(run_conversation("Hi, I'm wondering where my order PT-9923 is?"))
```

### Practice Activity
**Project exercise:** Add a second tool called `check_return_eligibility(order_id: str)` that returns whether an order is within the 30-day return window (use the fake order dates). Test with: "Can I return order PT-9923 and where is it currently?"

---

## Module 4 Project Checkpoint ✅

HelpBot now:
- Checks real (fake) order status using tools
- Handles cases where Claude needs multiple tool calls
- Gracefully reports tool errors back to Claude

---

---

# MODULE 5: Smarter Prompts & Speed

**Module outcomes:** Write more effective prompts; implement prompt caching for faster, cheaper responses.

**Total time:** ~2 hours

---

## Lesson 5.1 — Why Most Prompts Fail (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

Most developers write a prompt, test it once or twice, it sort of works, and they ship it. This is how you end up with AI features that work great in demos and fail in production.

**The evaluation mindset**

Treat your prompt like code. You wouldn't ship a function you'd only tested with one input — don't do it with prompts either.

A proper prompt evaluation pipeline:
1. Write a draft prompt
2. Create a set of test inputs (at least 10–20 diverse examples)
3. Run each test input through your prompt
4. Grade each output (is it correct? does it follow all constraints?)
5. Get an average score
6. Improve the prompt and repeat

The goal is an objective number that tells you whether prompt version B is better than version A — not a gut feeling.

---

## Lesson 5.2 — Making HelpBot's System Prompt Better (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

**Four techniques that consistently improve prompt performance:**

**1. Be clear and direct in your first line**
The first sentence of your prompt sets the frame for everything. Start with an action verb and a clear role:

❌ `"You are a helpful assistant for a bookstore."`
✅ `"Act as HelpBot, PageTurner Books' customer support agent. Your job is to resolve customer issues efficiently and warmly."`

**2. Be specific with attributes and steps**

Tell Claude not just *what* to do but *how* to approach it:

```
When handling a complaint:
1. Acknowledge the customer's frustration genuinely (not just "I understand")
2. Identify the specific issue (order problem, product quality, shipping)
3. Provide a concrete next step, not just "we'll look into it"
4. If you cannot resolve it, explain clearly who can and how to reach them
```

**3. Use XML tags to separate content blocks**

When you're inserting customer data or context into a prompt, wrap it clearly:

```python
prompt = f"""
Here is the customer's recent order history for context:
<order_history>
{customer_order_json}
</order_history>

Now respond to their current message: {customer_message}
"""
```

This helps Claude distinguish between data and instructions — especially important with large context blocks.

**4. Provide examples of ideal responses**

```
Here is an example of an ideal response to a damaged book complaint:

<example>
User: My book arrived with a ripped cover.
HelpBot: Oh no, I'm sorry to hear that — a damaged book is such a disappointment, 
especially when you're excited to read it. I'm going to get this sorted for you 
right away. Could you share your order number so I can pull up your details and 
arrange a replacement or refund, whichever you prefer?
</example>
```

### Practice Activity
**Guided exercise:** Apply all four techniques to rewrite the HelpBot system prompt. Then test the old vs. new version with 5 identical customer messages and rate each response on a 1–5 scale for helpfulness and personality. Did the score improve?

---

## Lesson 5.3 — Prompt Caching: Speed Without the Wait (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 25 min

### Core Content

**The problem prompt caching solves**

Every API request, Claude processes your entire input from scratch — including your system prompt, which might be 500 tokens and identical in every single request. That's a lot of repeated work.

Prompt caching lets you tell the API: "store the result of processing this content, and reuse it next time if you see the same thing." On cache hits, you get dramatically faster responses and pay a lower rate for input tokens.

**How to enable it**

Add `cache_control` to the blocks you want cached. The cache lasts up to 1 hour.

```python
# Cache the system prompt
system = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"}  # ← This line enables caching
    }
]

# Cache the tool schemas (add to the last tool)
tools_with_cache = TOOLS.copy()
tools_with_cache[-1] = {**tools_with_cache[-1], "cache_control": {"type": "ephemeral"}}

response = client.messages.create(
    model=MODEL,
    max_tokens=500,
    system=system,         # Pass as a list now, not a string
    messages=messages,
    tools=tools_with_cache,
    temperature=0.3
)
```

**Checking cache behaviour**

Look at the response usage:
- `response.usage.cache_creation_input_tokens` — tokens written to cache (first request)
- `response.usage.cache_read_input_tokens` — tokens read from cache (subsequent requests)

### Practice Activity
**Experiment:** Make 3 requests to HelpBot with caching enabled. Print the usage stats for each. Notice that the first request creates the cache; the second and third read from it. The total input tokens should be significantly lower from request 2 onwards.

---

## Module 5 Project Checkpoint ✅

HelpBot now has a professionally crafted system prompt and responds faster thanks to caching.

---

---

# MODULE 6: HelpBot Learns from Documents (RAG)

**Module outcomes:** Build a complete RAG pipeline to search PageTurner's policy documents.

**Total time:** ~3.5 hours

---

## Lesson 6.1 — What is RAG and Why Do We Need It? (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook
Imagine PageTurner has a 50-page return policy document, a shipping FAQ, and 200 product descriptions. A customer asks: "Can I return a digital book if I've already downloaded it?" HelpBot doesn't know — it wasn't trained on PageTurner's documents. You could put the entire 50-page document in the system prompt, but that's slow, expensive, and Claude gets less accurate with very long contexts.

RAG — Retrieval Augmented Generation — solves this. Instead of giving Claude all documents at once, you find the *relevant bits* and give Claude only those.

### Core Content

**The two-phase RAG approach**

**Phase 1 — Pre-processing (done once, before users arrive):**
1. Break your documents into small chunks (paragraphs or sections)
2. Convert each chunk into a numerical "fingerprint" (an embedding) that captures its meaning
3. Store all fingerprints in a database

**Phase 2 — Query time (done for every user question):**
1. Convert the user's question into a fingerprint using the same method
2. Find the stored fingerprints most similar to the question's fingerprint
3. Retrieve the original text of those matching chunks
4. Add the chunks to HelpBot's prompt as context
5. Claude answers using that specific, relevant information

The key insight: you're not feeding Claude the whole library — you're finding the right pages and handing Claude just those.

---

## Lesson 6.2 — Chunking PageTurner's Policy Documents (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Core Content

**What chunking means**

You can't embed an entire 50-page document as one unit — it's too long for the embedding model, and a match to "can I return a digital book" would drag in 50 pages of irrelevant information. You need smaller pieces.

**Strategy 1: Size-based chunking with overlap**

```python
def chunk_by_size(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Splits text into chunks of approximately `chunk_size` characters.
    Overlap ensures context isn't lost at chunk boundaries.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():  # Skip empty chunks
            chunks.append(chunk)
        start += chunk_size - overlap  # Move forward, but keep the last `overlap` chars
    return chunks
```

**Strategy 2: Structure-based chunking (better for formatted docs)**

```python
def chunk_by_section(markdown_text: str) -> list[str]:
    """
    Splits a markdown document at H2 headers (## Section Title).
    Best when documents have clear section structure.
    """
    sections = markdown_text.split("\n## ")
    # Re-add the ## that was split on
    return [("## " + s).strip() for s in sections if s.strip()]
```

**For PageTurner's policy docs:** They're structured markdown, so structure-based chunking is ideal.

### Practice Activity
**Guided exercise:** Create a fake `pageturner_returns_policy.md` file (5-6 sections covering: digital books, physical books, damaged items, timeframes, international orders, contact info). Run both chunking strategies on it and compare how many chunks each produces and whether each chunk makes sense in isolation.

---

## Lesson 6.3 — Text Embeddings: Teaching Claude to Search by Meaning (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 35 min

### Core Content

**What an embedding is**

An embedding model takes a piece of text and converts it into a long list of numbers — typically 1,000 to 4,000 numbers, depending on the model. These numbers aren't random. Similar texts produce similar lists of numbers.

If "I want to return a book" and "How do I send a book back?" both produce very similar number-lists, then they have similar *meaning* — even though they share no words.

That's the superpower: searching by meaning rather than by keyword.

**Setting up Voyage AI (Anthropic's recommended embedding provider)**

```bash
pip install voyageai
```

```python
import voyageai
import os

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

def generate_embedding(text: str) -> list[float]:
    """Converts text into a numerical embedding vector."""
    result = voyage_client.embed(
        texts=[text],
        model="voyage-3"
    )
    return result.embeddings[0]

def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Converts multiple texts into embeddings in one API call (more efficient)."""
    result = voyage_client.embed(
        texts=texts,
        model="voyage-3"
    )
    return result.embeddings
```

**What does "similar" mean mathematically?**

Similarity between two embeddings is calculated using cosine similarity — the cosine of the angle between the two vectors. A result of 1.0 means identical meaning, 0 means completely unrelated, -1 means opposite.

In practice, you'll often use cosine *distance* (1 - cosine similarity), where 0 = identical and higher = less similar.

---

## Lesson 6.4 — Building HelpBot's Document Search (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

**A simple in-memory vector store**

```python
import numpy as np

class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.documents = []
    
    def add(self, embedding: list[float], text: str):
        self.embeddings.append(np.array(embedding))
        self.documents.append(text)
    
    def search(self, query_embedding: list[float], top_k: int = 3) -> list[str]:
        """Returns the top_k most similar documents to the query."""
        query_vec = np.array(query_embedding)
        similarities = []
        
        for i, doc_embedding in enumerate(self.embeddings):
            # Cosine similarity calculation
            similarity = np.dot(query_vec, doc_embedding) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_embedding)
            )
            similarities.append((similarity, self.documents[i]))
        
        # Sort by similarity (highest first) and return top_k texts
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in similarities[:top_k]]
```

**Building the index from PageTurner's policy docs**

```python
store = VectorStore()

# Chunk the policy document
policy_text = open("pageturner_returns_policy.md").read()
chunks = chunk_by_section(policy_text)

# Generate embeddings for all chunks at once
print(f"Generating embeddings for {len(chunks)} chunks...")
embeddings = generate_embeddings_batch(chunks)

# Store everything
for chunk, embedding in zip(chunks, embeddings):
    store.add(embedding, chunk)

print("Document index built!")
```

**Searching the index**

```python
def search_policy_docs(question: str, top_k: int = 2) -> str:
    """Returns the most relevant policy chunks for a given question."""
    query_embedding = generate_embedding(question)
    relevant_chunks = store.search(query_embedding, top_k=top_k)
    return "\n\n---\n\n".join(relevant_chunks)

# Test
result = search_policy_docs("Can I return a digital ebook after downloading?")
print(result)
```

**Integrating RAG into HelpBot**

```python
RAG_SYSTEM_PROMPT = SYSTEM_PROMPT + """

When answering questions about PageTurner's policies, returns, or shipping,
use ONLY the information provided in the <policy_context> section below.
If the answer isn't in the context, say so honestly rather than guessing.
"""

def run_conversation_with_rag(user_input: str) -> str:
    # Step 1: Find relevant policy chunks
    relevant_context = search_policy_docs(user_input)
    
    # Step 2: Build messages with context injected
    messages = []
    augmented_message = f"""
<policy_context>
{relevant_context}
</policy_context>

Customer question: {user_input}
"""
    add_user_message(messages, augmented_message)
    
    # Step 3: Run normal conversation (with or without tools)
    return run_conversation_from_messages(messages, RAG_SYSTEM_PROMPT)
```

### Practice Activity
**Project exercise:** Build the full pipeline with your fake policy document. Test with 5 questions — some answerable from the docs (e.g. "Can I return a damaged book?") and some not (e.g. "Do you sell gift cards?"). Check that HelpBot says "I don't have that information" for the latter rather than making something up.

---

## Lesson 6.5 — Hybrid Search: Meaning + Keywords Together (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 30 min

### Core Content

**The limitation of semantic search alone**

Embedding search is great at finding *meaning* — but can miss specific technical terms. If PageTurner has a policy specifically about "ISBN returns" and a customer asks "what's the ISBN return policy", semantic search might return chunks about general returns rather than the specific ISBN section.

**BM25: matching by keywords**

BM25 (Best Match 25) is a classic keyword-based ranking algorithm. It finds documents that contain your search terms, weighting rare terms more heavily than common ones.

```bash
pip install rank-bm25
```

```python
from rank_bm25 import BM25Okapi

class BM25Store:
    def __init__(self):
        self.documents = []
        self.bm25 = None
    
    def add_documents(self, docs: list[str]):
        self.documents = docs
        tokenized = [doc.lower().split() for doc in docs]
        self.bm25 = BM25Okapi(tokenized)
    
    def search(self, query: str, top_k: int = 3) -> list[str]:
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)
        top_indices = scores.argsort()[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]
```

**Combining results with Reciprocal Rank Fusion**

```python
def hybrid_search(query: str, top_k: int = 3) -> list[str]:
    """
    Combines semantic and keyword search results using Reciprocal Rank Fusion.
    Documents that rank highly in BOTH methods get boosted.
    """
    semantic_results = store.search(generate_embedding(query), top_k=top_k)
    keyword_results = bm25_store.search(query, top_k=top_k)
    
    # Score each document based on its rank in each method
    scores = {}
    for rank, doc in enumerate(semantic_results):
        scores[doc] = scores.get(doc, 0) + 1 / (rank + 1)
    for rank, doc in enumerate(keyword_results):
        scores[doc] = scores.get(doc, 0) + 1 / (rank + 1)
    
    # Sort by combined score
    sorted_docs = sorted(scores.keys(), key=lambda d: scores[d], reverse=True)
    return sorted_docs[:top_k]
```

### Practice Activity
**Experiment:** Create a policy chunk that mentions a very specific term (e.g. "ISBN-based returns"). Then test semantic search vs. hybrid search when a customer asks about it. Does hybrid search perform better?

---

## Module 6 Project Checkpoint ✅

HelpBot now:
- Chunks and indexes PageTurner's policy documents
- Searches by meaning using embeddings
- Combines semantic + keyword search for better accuracy
- Grounds its answers in real policy content

---

---

# MODULE 7: Finishing HelpBot & Going Further

**Module outcomes:** Handle PDFs and images; assemble the complete HelpBot; understand the path forward.

**Total time:** ~2 hours

---

## Lesson 7.1 — Reading PDFs and Analysing Images (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 30 min

### Core Content

**PDF support**

Claude can read PDF files directly — no need to extract text first. The implementation mirrors image input almost exactly.

```python
import base64

def ask_about_pdf(pdf_path: str, question: str) -> str:
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",       # ← "document" for PDFs
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_b64
                    },
                    "title": "PageTurner Returns Policy"
                },
                {
                    "type": "text",
                    "text": question
                }
            ]
        }]
    )
    return response.content[0].text
```

**Image support**

```python
def ask_about_image(image_path: str, question: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",  # or image/png, image/webp
                        "data": image_b64
                    }
                },
                {
                    "type": "text",
                    "text": question
                }
            ]
        }]
    )
    return response.content[0].text
```

**HelpBot application:** A customer can attach a photo of their damaged book. HelpBot analyses the image and automatically categorises the damage type before creating a return request.

---

## Lesson 7.2 — The Complete HelpBot (Workshop)
**Type:** Workshop | **Duration:** 45 min

### Core Content

This is your assembly lesson. You'll bring together every piece built across all modules into one cohesive `helpbot.py` file.

**Final HelpBot architecture:**

```
helpbot.py
├── Configuration (API client, model, system prompt)
├── Document Index (RAG pipeline - built at startup)
├── Tools (check_order_status, check_return_eligibility, + schemas)
├── Core Functions
│   ├── hybrid_search(query) → relevant chunks
│   ├── run_tool(name, input) → tool result
│   ├── process_tool_calls(content) → tool results list
│   └── chat_with_rag(user_input, history) → reply text
└── Main loop (command-line interface)
```

**The main conversation loop**

```python
def main():
    print("Welcome to PageTurner Books Support! I'm HelpBot.")
    print("Type 'quit' to exit.\n")
    
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("Thanks for contacting PageTurner. Happy reading!")
            break
        
        reply = chat_with_rag(user_input, conversation_history)
        print(f"\nHelpBot: {reply}\n")

if __name__ == "__main__":
    main()
```

### Project Activity
**Final project:** Assemble the complete `helpbot.py`, test it with a realistic 5-turn customer service scenario (damaged book → return request → order check → confirmation), and document any failures or unexpected behaviours you observe.

---

## Lesson 7.3 — What's Next? The Bigger Picture (Concept)
**Type:** Concept | **Duration:** 25 min

### Core Content

You've built a real, working AI application. But we've only scratched the surface of what the Claude API can do. Here's a brief map of what's ahead if you keep building:

**Agents & Workflows**

A workflow is a fixed sequence of Claude calls for a known task — like: get user's query → search docs → draft reply → check for policy violations → send. Workflows are reliable because the steps are predictable.

An agent is different: you give Claude a set of tools and let it decide *which* tools to use and in *what* order to solve a problem it hasn't seen before. More flexible, harder to predict.

For HelpBot: a workflow would generate a standardised complaint report. An agent might autonomously troubleshoot a complex multi-step order issue.

**MCP — Model Context Protocol**

Instead of writing tool schemas and functions yourself for every service (Slack, Jira, GitHub, databases), MCP is a standardised way for Claude to connect to pre-built integrations. The community builds MCP servers; you just connect to them.

**Claude Code**

A terminal-based AI coding assistant built on these same APIs. It can read your project files, write code, run tests, and even make Git commits — all from your terminal. Great for seeing how a real agentic product is built on top of the API.

**Extended Thinking**

For genuinely hard reasoning tasks — complex multi-step analysis, strategy, evaluating trade-offs — you can give Claude a "thinking budget" and it will reason step-by-step before producing its final answer. More accurate, more expensive, worth it for the right tasks.

---

## Final Project

**Build your own HelpBot variant.**

Choose a different business type (restaurant, gym, software company) and build a working support chatbot that has:
- ✅ Multi-turn conversation memory
- ✅ A custom system prompt with clear persona
- ✅ At least two tools
- ✅ Streaming responses
- ✅ RAG from at least one document (you write the fake doc)
- ✅ Structured output for at least one use case (e.g. booking request form)

**Rubric:**
| Component | Full marks | Partial | None |
|-----------|-----------|---------|------|
| System prompt quality | 20 | 10 | 0 |
| Multi-turn memory works | 20 | 10 | 0 |
| At least 2 tools functional | 20 | 10 | 0 |
| RAG pipeline retrieves relevant chunks | 20 | 10 | 0 |
| Structured JSON output works | 10 | 5 | 0 |
| Streaming implemented | 10 | 5 | 0 |

**Total: 100 points**

---

---

# Appendix: Assessment Design

## Module Quizzes (5 questions each)

**Module 1 Quiz Topics:** model selection trade-offs, what a token is, reading the response object, stop_reason values, input vs output tokens

**Module 2 Quiz Topics:** why the API has no memory, message roles, what a system prompt is and isn't, temperature settings for different use cases, multi-turn conversation structure

**Module 3 Quiz Topics:** streaming event types, when to use prefilling, stop sequence behaviour, structured output pattern, what `flush=True` does in print statements

**Module 4 Quiz Topics:** the 5-step tool use flow, what tool_use_id is for, is_error flag, while loop necessity, what happens if a tool function throws an exception

**Module 5 Quiz Topics:** what prompt evaluation gives you that manual testing doesn't, Bloom's taxonomy applied to prompt design, cache invalidation rules, cache_read vs cache_creation tokens, temperature for eval grading

**Module 6 Quiz Topics:** why chunking is needed, overlap in size-based chunking, what an embedding is, cosine similarity scale, RRF formula intuition

---

## Assignments

**Assignment 1 (After Module 2):** Redesign HelpBot's system prompt for a completely different business type. Write before/after comparisons of responses to 3 questions.

**Assignment 3 (After Module 3):** Build a JSON extraction pipeline for a different use case — e.g. extract complaint categories and urgency from 10 customer reviews.

**Assignment 4 (After Module 4):** Add a third tool to HelpBot: `get_estimated_restock_date(book_title: str)` that returns when an out-of-stock book will be back. Integrate it into a multi-turn conversation where a customer asks about an unavailable title.

**Final Project (After Module 7):** See Final Project section above.

---

## Notes for Course Expansion

- Each lesson script above can be expanded with 2–3x more depth for video delivery — the code examples are the foundation
- Consider adding supplementary "common errors" sections for Lessons 1.3, 3.2, and 4.3 — these are where beginners most often get stuck
- Module 5 (Prompt Engineering) can be expanded significantly with a full evaluation pipeline walkthrough including grading rubrics
- Module 6 could add a lesson on reranking with a Claude-based grader for more advanced students
- For a live cohort version, Lessons 7.2 (final assembly) and the Final Project work well as group workshop sessions
