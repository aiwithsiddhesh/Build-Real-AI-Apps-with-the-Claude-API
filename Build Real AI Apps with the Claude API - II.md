# Build Production AI Systems with the Claude API
## Series 2 of 3 — Intermediate

> **Prerequisite:** Beginner Claude API Course (or equivalent — you should be comfortable making API calls, building multi-turn conversations, basic tool use, and basic RAG)
> **Format:** Self-paced | **Duration:** 15–20 hours | **Skill Level:** Intermediate Python developer

---

## How This Course Is Different From the Beginner Course

The beginner course taught you *how* the Claude API works. This course teaches you how to build AI systems that actually hold up — reliably, under real conditions, with real users.

The shift in mindset:

| Beginner thinking | Intermediate thinking |
|---|---|
| "It works when I test it" | "It works consistently across 100 different inputs" |
| "I'll test it manually" | "I have an eval pipeline with objective scores" |
| "One Claude call per task" | "Multi-step workflows with branching and parallelism" |
| "It retrieves something" | "It retrieves the *right* thing, reranked by relevance" |
| "Claude uses tools" | "Claude uses tools in parallel, with graceful failure" |
| "I write tool schemas myself" | "MCP servers handle integrations for me" |

If the beginner course was learning to drive — intermediate is learning to drive on a highway, in traffic, with a deadline.

---

## The Single Project: BriefBot — AI Research Briefing Engine

**BriefBot** takes any research topic and produces a structured, cited, professionally formatted research briefing. Think of it as an AI research analyst: you give it a question, it goes to work — classifying the topic, researching multiple angles in parallel, searching its knowledge base, reasoning deeply about the findings, and returning a complete document you can actually use.

**What a BriefBot output looks like:**

```json
{
  "topic": "The impact of weight-loss drugs on the food industry",
  "topic_category": "business",
  "executive_summary": "GLP-1 drugs are reshaping food consumption patterns...",
  "sections": [
    {
      "title": "Market Context",
      "content": "The global GLP-1 market is expected to reach $130B by 2030...",
      "citations": [
        {"source_id": "src_001", "quoted_text": "projected market size of $130B"}
      ]
    },
    {
      "title": "Industry Response",
      "content": "Major food manufacturers are reformulating products...",
      "citations": [...]
    },
    {
      "title": "Risks & Unknowns",
      "content": "Long-term effects on consumption patterns remain uncertain...",
      "citations": [...]
    },
    {
      "title": "Strategic Outlook",
      "content": "Companies that adapt product lines early are likely to...",
      "citations": [...]
    }
  ],
  "key_findings": [
    "GLP-1 drugs reduce caloric intake by 20–30% on average",
    "Snack and sugary drink categories face the greatest disruption",
    "Health-focused product lines showing 15% higher growth in 2024"
  ],
  "confidence_level": "high",
  "sources": [
    {"id": "src_001", "title": "Goldman Sachs GLP-1 Report", "url": "..."}
  ],
  "metadata": {
    "generated_at": "2026-06-13T10:30:00Z",
    "model": "claude-sonnet-4-6",
    "tokens_used": 4821,
    "thinking_tokens": 1024
  }
}
```

Every module of this course adds a new capability to BriefBot. By the end, it will:

- Classify topics and route them to the right research pipeline
- Research multiple angles simultaneously (parallelization)
- Search a knowledge base with contextual retrieval and LLM reranking
- Reason deeply using extended thinking before synthesising
- Output fully cited briefings linked to source documents
- Connect to external services through MCP

And you'll have an eval pipeline measuring how good every version is.

---

## Learner Persona

**Name:** Priya — The Developer Who Wants to Ship

**Who she is:** A developer with 1–2 years of Python experience who completed the beginner Claude API course (or equivalent). She's built a chatbot or two, integrated Claude into a side project, and can call the API in her sleep. Now she has a real use case — at work or as a product — and "it kind of works" isn't good enough anymore.

**What she knows coming in:**
- Comfortable Python (functions, classes, async is not foreign)
- Claude API basics: messages, system prompts, tools, basic RAG, streaming
- Has built at least one AI-powered feature end to end

**What she wants:**
- Prompts that work reliably, not just sometimes
- AI workflows she can explain to a colleague or stakeholder
- Systems she can test and improve with data, not gut feelings
- To understand the production patterns that real AI teams use

**The gap:**
- No formal approach to evaluating AI output
- Has written prompts by trial and error, not systematic engineering
- Hasn't built multi-step workflows with branching logic
- RAG works but she doesn't know how to make it more accurate
- Has heard of MCP but hasn't built or connected to a server

**Time available:** ~3–4 hours per week
**Format:** Self-paced, code-heavy, project-based

**Success looks like:** Priya ships BriefBot as a working internal tool at her company, with a documented eval pipeline showing 8.2/10 average briefing quality.

---

## Course-Level Learning Outcomes

By the end of this course, learners will be able to:

1. **Build** a prompt evaluation pipeline with automated code-based and LLM-based graders
2. **Design** AI workflows using chaining, routing, and parallelization patterns
3. **Implement** the evaluator-optimizer loop to iteratively improve AI output quality
4. **Apply** advanced RAG techniques — contextual retrieval, hybrid search, and LLM reranking
5. **Create** reliable structured output pipelines using tool schemas and parallel tool execution
6. **Enable** extended thinking for complex multi-step reasoning tasks
7. **Build** a basic MCP server and client to connect Claude to external services

---

## Module Map

| # | Module | Key Outcomes | BriefBot Milestone | Est. Time |
|---|--------|--------------|--------------------|-----------|
| 1 | From Demo to Production | — | BriefBot skeleton + architecture plan | 1.5 hrs |
| 2 | Evaluating AI Output Like an Engineer | 1 | BriefBot has a working eval pipeline | 2.5 hrs |
| 3 | Systematic Prompt Engineering | 1, 3 | BriefBot prompts score 7+ on eval | 2 hrs |
| 4 | AI Workflows: Chain, Route, Parallelize | 2 | BriefBot's full research pipeline | 3 hrs |
| 5 | Advanced RAG | 4 | BriefBot retrieves with context + reranking | 2.5 hrs |
| 6 | Advanced Tools & Structured Output | 5 | BriefBot extracts structured data in parallel | 2 hrs |
| 7 | Extended Thinking & Citations | 6 | BriefBot reasons deeply and cites sources | 1.5 hrs |
| 8 | Intro to MCP | 7 | BriefBot connects to an MCP server | 2.5 hrs |
| 9 | Final Assembly + What Comes Next | All | Complete BriefBot, production-ready | 1.5 hrs |

**Total: ~19.5 hours**

---
---

# MODULE 1: From Demo to Production

**Module outcome:** Understand what separates a reliable AI system from a fragile demo; set up the BriefBot project architecture.

**Total time:** ~1.5 hours

---

## Lesson 1.1 — The Production Gap (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook

You've shipped something. It works in your testing. You show a colleague — works. You deploy it — and then a real user types something you didn't anticipate, and it breaks. Or worse: it doesn't break, it just quietly produces a bad answer that the user acts on.

This is the production gap: the distance between "works on the inputs I tested" and "works reliably across the messy, unpredictable range of real inputs."

In traditional software, you close this gap with unit tests, integration tests, and type safety. With AI systems, the same instinct applies — but the tools look different. You use *eval pipelines* instead of test suites. You use *workflows* instead of single-function calls. You use *graders* instead of assertions.

### Core Content

**The five failure modes of amateur AI systems:**

1. **Prompt brittleness** — The prompt works for the happy path but breaks on unexpected input. A user asks the question slightly differently and the output degrades dramatically.

2. **No measurement** — You have no objective way to tell if version B of your prompt is better than version A. You're improving by feel, which means you're not really improving systematically.

3. **Monolithic architecture** — One giant Claude call trying to do everything. Research, synthesise, format, validate — all in one. When it fails, you have no idea which step went wrong.

4. **Brittle retrieval** — Your RAG pipeline returns *something* but not necessarily the *right* thing. Chunks lack context. Keyword mismatches go unhandled. There's no second pass to verify relevance.

5. **Hard dependencies** — One tool fails, the whole thing crashes. No retry logic, no graceful degradation, no fallback.

The intermediate course is designed to close all five gaps — one module at a time.

---

## Lesson 1.2 — Introducing BriefBot (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 30 min

### Core Content

**BriefBot's architecture — top level**

```
User gives a topic
       ↓
[Module 1] Topic Classification → what category is this?
       ↓
[Module 4] Route to the right research pipeline
       ↓
[Module 4] Parallel research → 4 angles simultaneously
       ↓
[Module 5] RAG search → pull relevant knowledge base chunks
       ↓
[Module 7] Extended thinking synthesis → reason deeply about findings
       ↓
[Module 7] Citation extraction → link claims to sources
       ↓
Structured JSON briefing output
```

**The skeleton — what we build in Module 1**

A basic version with no intelligence yet. Just the scaffolding: project structure, configuration, basic API connection, and a stub function that takes a topic and returns a placeholder briefing.

```
briefbot/
├── main.py              # Entry point
├── config.py            # API keys, model names, constants
├── briefbot.py          # Core BriefBot class
├── workflows/
│   ├── chain.py         # Chaining workflow
│   ├── router.py        # Routing workflow
│   └── parallel.py      # Parallelization workflow
├── rag/
│   ├── chunker.py       # Text chunking
│   ├── embedder.py      # Voyage AI embeddings
│   ├── vector_store.py  # Vector similarity search
│   └── retriever.py     # Full RAG retriever
├── tools/
│   ├── schemas.py       # Tool schemas
│   └── executor.py      # Tool execution
├── eval/
│   ├── dataset.py       # Test dataset management
│   ├── runner.py        # Eval pipeline runner
│   └── graders.py       # Code + model graders
└── knowledge_base/
    └── articles/        # Sample research articles for RAG
```

**config.py — shared configuration**

```python
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
MODEL = "claude-sonnet-4-6"
EVAL_MODEL = "claude-haiku-4-5-20251001"  # Cheaper model for grading
EMBEDDING_MODEL = "voyage-3"
MAX_TOKENS = 4000
EVAL_MAX_TOKENS = 1000
TEMPERATURE = 0.3
```

**briefbot.py — the stub class**

```python
import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS, TEMPERATURE

class BriefBot:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    def generate_briefing(self, topic: str) -> dict:
        """
        Generates a research briefing for the given topic.
        Returns a structured dict with sections, findings, and metadata.
        """
        # Stub: returns placeholder for now
        # We'll replace this step by step across the course
        return {
            "topic": topic,
            "executive_summary": "Placeholder — to be implemented",
            "sections": [],
            "key_findings": [],
            "confidence_level": "low",
            "sources": [],
            "metadata": {"model": MODEL}
        }

if __name__ == "__main__":
    bot = BriefBot()
    result = bot.generate_briefing("The future of solar energy storage")
    print(result)
```

### Practice Activity
**Setup task:** Create the full folder structure, install dependencies (`pip install anthropic python-dotenv voyageai rank-bm25 numpy`), and confirm `python main.py` runs without errors on the stub.

---

## Lesson 1.3 — Thinking in Systems (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**One principle that changes everything: decompose for testability**

Every step in an AI system should be independently testable. If you can't test a step in isolation, you can't tell whether a failure is in *that* step or one that feeds into it.

For BriefBot, this means:
- The classifier can be tested independently: does it correctly categorise 20 sample topics?
- The retriever can be tested independently: does it return relevant chunks for 20 queries?
- The synthesis step can be tested independently: given the same inputs, does it produce good output?

This isolation is what lets you iterate fast. When your eval score drops after a change, you know *which module* got worse — not just that something broke somewhere.

**The eval-first mindset**

In this course, every time we add a new feature to BriefBot, we run an eval *before and after*. Not just "does it work?" — but "did the score go up?" This discipline is what separates engineers who ship reliable AI systems from engineers who ship demos that got lucky.

### Wrap-Up
BriefBot's skeleton is live. You understand why decomposition and testability matter. In Module 2, we build the eval pipeline that will guide every improvement we make for the rest of the course.

---

## Module 1 Project Checkpoint ✅
BriefBot is scaffolded. The project structure is clean and every component has a clear home.

---
---

# MODULE 2: Evaluating AI Output Like an Engineer

**Module outcome:** Build a prompt evaluation pipeline with automated code-based and LLM-based graders.

**Total time:** ~2.5 hours

---

## Lesson 2.1 — The Eval Problem (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook

Here's a question most developers never ask: *How do you know your last prompt change made things better?*

If the answer is "it seemed better when I tested it" — that's a problem. Your intuition is optimised for the examples you happened to try. It's blind to edge cases. It has no memory of what "before" actually looked like across 50 inputs.

The only honest answer is a number. An average quality score across a diverse set of test inputs, measured consistently before and after every change.

### Core Content

**The eval pipeline — 5 components:**

```
Test Dataset  →  Prompt Template  →  LLM  →  Grader  →  Score
(test inputs)    (your prompt)       (Claude)  (code or LLM)  (0–10)
```

1. **Test Dataset** — A collection of inputs that represent the range your prompt will face in production. Not just the easy cases.

2. **Prompt Template** — Your current prompt, with placeholders for test inputs.

3. **LLM** — Claude processes each test case and produces an output.

4. **Grader** — Something scores each output. Two types: code graders (fast, rule-based) and model graders (flexible, LLM-based).

5. **Score** — The average across all test cases. This is your metric. You want this number to go up with every prompt change.

**Three paths after writing a prompt:**

1. Ship it after testing once (trap)
2. Tweak it until a few manual tests look good (also a trap)
3. Run it through an eval pipeline and get an objective score (correct)

---

## Lesson 2.2 — Building BriefBot's Test Dataset (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Core Content

**What a good test dataset looks like**

For BriefBot, each test case is a research topic. You want:
- A range of topic categories (business, academic, technical, news)
- Different complexity levels (narrow vs. broad)
- Some genuinely hard cases (ambiguous topics, niche subjects)
- At least 20 examples (more is better; start here)

**Generating a dataset automatically with Claude**

Rather than writing 20 topics by hand, use Haiku (fast and cheap) to generate them:

```python
# eval/dataset.py
import json
import anthropic
from config import ANTHROPIC_API_KEY, EVAL_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

DATASET_GENERATION_PROMPT = """
Generate 20 diverse research briefing topics for testing an AI research engine.

Requirements:
- Mix of categories: business (5), academic (5), technical (5), news/current events (5)
- Vary complexity: some narrow and specific, some broad
- Include at least 3 genuinely challenging or ambiguous topics
- Each topic should be a clear, specific research question or subject

Respond ONLY with a JSON array of objects. No preamble, no markdown.
Each object must have: "topic" (string) and "category" (string: business/academic/technical/news)
"""

def generate_dataset(output_path: str = "eval/dataset.json") -> list[dict]:
    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": DATASET_GENERATION_PROMPT}],
        # Prefill forces raw JSON output
    )
    
    dataset = json.loads(response.content[0].text)
    
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Generated {len(dataset)} test cases → {output_path}")
    return dataset

def load_dataset(path: str = "eval/dataset.json") -> list[dict]:
    with open(path) as f:
        return json.load(f)
```

**Sample output:**
```json
[
  {"topic": "The role of microbiome research in personalised nutrition", "category": "academic"},
  {"topic": "Impact of interest rate hikes on commercial real estate 2024", "category": "business"},
  {"topic": "Quantum error correction: current approaches and timeline", "category": "technical"},
  {"topic": "AI regulation legislation in the EU: current state and gaps", "category": "news"},
  ...
]
```

### Practice Activity
**Run it:** Generate your dataset and review the 20 topics. Do they look appropriately diverse? Add 5 more manually that you think are edge cases for BriefBot. Save the final 25-topic dataset.

---

## Lesson 2.3 — Running the Eval Pipeline (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Core Content

**The runner — processing every test case**

```python
# eval/runner.py
import json
import time
from briefbot import BriefBot
from eval.graders import grade_output

def run_prompt(bot: BriefBot, test_case: dict) -> dict:
    """Runs a single test case through BriefBot."""
    start = time.time()
    output = bot.generate_briefing(test_case["topic"])
    elapsed = time.time() - start
    return {
        "test_case": test_case,
        "output": output,
        "latency_seconds": round(elapsed, 2)
    }

def run_eval(dataset: list[dict], bot: BriefBot) -> dict:
    """Runs all test cases and returns aggregate results."""
    results = []
    scores = []
    
    for i, test_case in enumerate(dataset):
        print(f"Running test case {i+1}/{len(dataset)}: {test_case['topic'][:50]}...")
        result = run_prompt(bot, test_case)
        grade = grade_output(result["output"], test_case)
        result["grade"] = grade
        scores.append(grade["score"])
        results.append(result)
    
    return {
        "results": results,
        "average_score": round(sum(scores) / len(scores), 2),
        "min_score": min(scores),
        "max_score": max(scores),
        "total_cases": len(dataset)
    }
```

**Running it from main.py**

```python
# main.py
from briefbot import BriefBot
from eval.dataset import load_dataset, generate_dataset
from eval.runner import run_eval
import json

bot = BriefBot()
dataset = load_dataset()

print("Running eval...")
results = run_eval(dataset, bot)

print(f"\n=== EVAL RESULTS ===")
print(f"Average score: {results['average_score']} / 10")
print(f"Range: {results['min_score']} – {results['max_score']}")
print(f"Total cases: {results['total_cases']}")
```

With the stub BriefBot, you'll get a score near 0 — expected. This is your baseline. Every improvement you make to BriefBot will (should) raise this number.

---

## Lesson 2.4 — Code-Based Grading (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 25 min

### Core Content

**What code graders check**

Code graders are fast, free (no API call needed), and objective. They validate structural correctness — not quality. For BriefBot, good code graders check:

- Is the output a valid dict?
- Does it have all required fields (`topic`, `executive_summary`, `sections`, `key_findings`)?
- Does it have at least 2 sections?
- Does it have at least 3 key findings?
- Are citations present in at least one section?

```python
# eval/graders.py
def code_grade(output: dict) -> tuple[float, list[str]]:
    """
    Validates structural completeness of a BriefBot output.
    Returns (score 0–5, list of issues found).
    """
    issues = []
    score = 5.0
    
    required_fields = ["topic", "executive_summary", "sections", "key_findings", "sources"]
    for field in required_fields:
        if field not in output or not output[field]:
            issues.append(f"Missing or empty field: '{field}'")
            score -= 1.0
    
    if "sections" in output:
        if len(output["sections"]) < 2:
            issues.append("Fewer than 2 sections")
            score -= 0.5
        
        sections_with_citations = [s for s in output["sections"] if s.get("citations")]
        if not sections_with_citations:
            issues.append("No sections contain citations")
            score -= 0.5
    
    if "key_findings" in output and len(output.get("key_findings", [])) < 3:
        issues.append("Fewer than 3 key findings")
        score -= 0.5
    
    return max(0.0, score), issues
```

---

## Lesson 2.5 — Model-Based Grading (LLM-as-a-Judge) (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Hook

Code graders check *structure*. But they can't tell you whether the executive summary is insightful or shallow, whether the sections cover the topic well, or whether the key findings are actually meaningful. For that, you need a model grader — Claude evaluating Claude's output.

### Core Content

**Why ask for reasoning before the score**

If you ask Claude "rate this on a scale of 1–10," it tends to cluster answers around 5–7 (safety bias). If you ask it to first describe *strengths*, then *weaknesses*, then justify a score — you get a much more calibrated number.

```python
# eval/graders.py (continued)
import anthropic
import json
from config import ANTHROPIC_API_KEY, EVAL_MODEL

_eval_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

MODEL_GRADER_PROMPT = """
You are evaluating the quality of an AI-generated research briefing.

<briefing>
{briefing_json}
</briefing>

Original research topic: {topic}

Evaluate this briefing across these dimensions:
1. Depth — Does it go beyond surface-level information?
2. Accuracy signals — Does anything seem invented or implausible?
3. Structure — Are sections well-organised and clearly titled?
4. Key findings quality — Are the findings specific and genuinely useful?
5. Coverage — Does it address the topic from multiple meaningful angles?

First list 2–3 specific strengths.
Then list 2–3 specific weaknesses or gaps.
Then provide a score from 1–10 and a one-sentence justification.

Respond ONLY with a JSON object. No markdown. No preamble.
Format: {"strengths": [...], "weaknesses": [...], "score": X, "justification": "..."}
"""

def model_grade(output: dict, test_case: dict) -> dict:
    """
    Uses an LLM to evaluate the quality of a BriefBot output.
    Returns a dict with strengths, weaknesses, score, and justification.
    """
    prompt = MODEL_GRADER_PROMPT.format(
        briefing_json=json.dumps(output, indent=2),
        topic=test_case["topic"]
    )
    
    response = _eval_client.messages.create(
        model=EVAL_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.content[0].text)
```

**Combining both graders into one score**

```python
def grade_output(output: dict, test_case: dict) -> dict:
    """
    Combines code-based (structural) and model-based (quality) grading.
    Final score = average of both, on a 0–10 scale.
    """
    code_score, code_issues = code_grade(output)
    model_result = model_grade(output, test_case)
    
    # Normalise code score to 0–10
    code_score_normalised = (code_score / 5.0) * 10
    model_score = model_result["score"]
    
    final_score = round((code_score_normalised + model_score) / 2, 1)
    
    return {
        "score": final_score,
        "code_score": code_score_normalised,
        "model_score": model_score,
        "code_issues": code_issues,
        "model_strengths": model_result["strengths"],
        "model_weaknesses": model_result["weaknesses"],
        "model_justification": model_result["justification"]
    }
```

### Practice Activity
**Run the full eval on your stub BriefBot.** Record the baseline score. It should be very low — that's fine. This number is now your target to beat. Every module that adds real capability to BriefBot should raise it.

### Module 2 Checkpoint ✅
BriefBot has a working eval pipeline. Baseline score is recorded. You'll re-run this at the end of every module.

---
---

# MODULE 3: Systematic Prompt Engineering

**Module outcome:** Apply advanced prompting techniques; implement the evaluator-optimizer loop.

**Total time:** ~2 hours

---

## Lesson 3.1 — The Four Core Techniques (Concept + Practice)
**Type:** Concept + Practice | **Duration:** 35 min

### Hook

If the beginner course introduced these techniques, this module is where you actually *use* them in a measured way — with before/after eval scores to confirm they're working.

### Core Content

You already know the four techniques from the beginner course. Here we apply them with discipline:

**1. Clear first line with action verb**

Your prompt's first sentence is the highest-leverage sentence in the whole thing. Claude reads it first and it sets the frame for everything that follows.

❌ Weak: `"You are an AI that helps with research."`
✅ Strong: `"Generate a structured research briefing on the given topic, with distinct sections, cited key findings, and a clear executive summary."`

**2. Specific attributes AND steps**

Type A (attributes) — describe what good output looks like:
```
The briefing must:
- Have 3–5 clearly titled sections covering distinct angles of the topic
- Include an executive summary of 2–3 concise paragraphs
- List exactly 4–6 specific, evidence-based key findings
- Assign a confidence level: high (well-documented), medium (mixed evidence), or low (speculative)
```

Type B (steps) — tell Claude how to think:
```
Approach the briefing in this order:
1. First, identify the topic category and the 3–4 most important questions a reader needs answered
2. For each question, write a dedicated section with clear supporting evidence
3. Synthesise the most impactful findings as bullet points
4. Assess confidence level based on how well-established the evidence appears
5. Only then write the executive summary — it should reflect the sections, not introduce new ideas
```

Combine both types in professional prompts.

**3. XML tags for variable content**

When you inject the user's topic into the prompt, wrap it:

```python
system_prompt = """
Generate a research briefing as described. Focus exclusively on the topic provided.
If the topic is ambiguous, pick the most common interpretation and note the assumption.
"""

user_message = f"""
<research_topic>
{topic}
</research_topic>

Generate the briefing now. Respond with a JSON object only — no markdown fences, no preamble.
"""
```

**4. One-shot examples**

Show Claude exactly what a great briefing looks like. Use XML to separate the example from the actual instruction:

```
<example>
Topic: "The impact of streaming on music revenue"

{
  "topic": "The impact of streaming on music revenue",
  "executive_summary": "Music streaming has fundamentally restructured revenue flows...",
  "sections": [
    {
      "title": "Revenue Shift from Sales to Streams",
      "content": "Physical and digital sales have declined 73% since 2012...",
      "citations": [{"source_id": "src_001", "quoted_text": "declined 73%"}]
    }
  ],
  "key_findings": ["Per-stream rates average $0.003–$0.005 across major platforms"],
  "confidence_level": "high",
  ...
}
</example>

Now generate the briefing for the topic provided.
```

### Practice Activity
**Eval sprint:** Write a BriefBot system prompt using all four techniques. Run the full eval. Compare your new score against the baseline. If the score improved — why? If it didn't — review which weaknesses the model grader is calling out most often.

---

## Lesson 3.2 — The Evaluator-Optimizer Pattern (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 45 min

### Hook

What if instead of you iterating on the prompt, BriefBot iterated on *its own output*? Generate a briefing, have Claude score it, and if the score is low — have Claude rewrite it using the weaknesses as a guide. This is the evaluator-optimizer pattern: a producer generates, an evaluator judges, a loop repeats until the output is good enough.

### Core Content

**The pattern**

```
Topic → [Generate Briefing] → [Evaluate] → Score < threshold?
                                               ↓ Yes
                                     [Regenerate with feedback]
                                               ↓
                                     [Evaluate again] → loop up to max_iterations
                               Score ≥ threshold?
                                               ↓ Yes
                                     Return briefing
```

**Implementation**

```python
# briefbot.py
import json
from config import MODEL, MAX_TOKENS, TEMPERATURE

class BriefBot:
    def __init__(self):
        # ... (client init)
        pass

    def _generate_once(self, topic: str, feedback: str = None) -> dict:
        """Single briefing generation pass. Accepts optional improvement feedback."""
        system = self._build_system_prompt()
        
        user_content = f"<research_topic>\n{topic}\n</research_topic>"
        if feedback:
            user_content += f"\n\n<improvement_feedback>\n{feedback}\n</improvement_feedback>\n\nPlease regenerate the briefing addressing all the weaknesses listed above."
        
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": user_content}],
            temperature=TEMPERATURE
        )
        
        return json.loads(response.content[0].text)

    def _evaluate_output(self, output: dict, topic: str) -> dict:
        """Uses model grader to score the output."""
        from eval.graders import grade_output
        return grade_output(output, {"topic": topic})

    def generate_briefing(
        self,
        topic: str,
        quality_threshold: float = 7.0,
        max_iterations: int = 3
    ) -> dict:
        """
        Generates a briefing, evaluates it, and reruns if below threshold.
        Returns the best version produced within max_iterations.
        """
        best_output = None
        best_score = 0.0

        for iteration in range(max_iterations):
            print(f"  Iteration {iteration + 1}/{max_iterations}...")
            
            # Generate
            feedback = None
            if best_output and best_score < quality_threshold:
                # Build feedback from the last evaluation
                last_grade = self._evaluate_output(best_output, topic)
                feedback = "Weaknesses identified:\n- " + "\n- ".join(last_grade["model_weaknesses"])
            
            output = self._generate_once(topic, feedback=feedback)
            grade = self._evaluate_output(output, topic)
            score = grade["score"]
            
            print(f"  Score: {score}/10")
            
            if score > best_score:
                best_score = score
                best_output = output
                best_output["metadata"]["eval_score"] = score
                best_output["metadata"]["iterations"] = iteration + 1

            if score >= quality_threshold:
                print(f"  ✓ Quality threshold reached on iteration {iteration + 1}")
                break
        
        return best_output
```

**Key design decisions:**
- We track the *best* output, not just the last one — in case quality oscillates
- We pass weaknesses specifically rather than a generic "try again"
- We cap at `max_iterations` to control cost

### Practice Activity
**Test it:** Run `generate_briefing("The rise of sovereign AI clouds", max_iterations=3)` and print the score at each iteration. Does it improve? Run the full eval again — does the pipeline-level average score improve with the optimizer loop active?

---

## Module 3 Checkpoint ✅
BriefBot now has a scored prompt, a tracked eval baseline, and a self-improving optimization loop.

---
---

# MODULE 4: AI Workflows — Chain, Route, Parallelize

**Module outcome:** Design and implement chaining, routing, and parallelization workflows.

**Total time:** ~3 hours

---

## Lesson 4.1 — Workflows vs Agents: Picking Your Tool (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

This distinction matters more as systems get complex:

**A workflow** is a fixed sequence of Claude calls where *you* decide the steps in advance. You control the logic. Claude executes each step. Reliable, predictable, testable.

**An agent** gives Claude a toolbox and says "figure out the steps yourself." Flexible but unpredictable. Harder to evaluate. Better suited for open-ended tasks where you genuinely don't know the right steps.

**For BriefBot:** We use workflows. We know the research process — classify, plan, research, synthesise, format. These steps don't change per topic. What changes is the *content* at each step, not the structure. That's a workflow job.

Rule of thumb: if you can write the flowchart in advance, use a workflow. If you'd need a flowchart with a question mark in the middle, consider an agent.

---

## Lesson 4.2 — Chaining: Building BriefBot's Research Pipeline (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Hook

Right now, BriefBot does everything in one giant Claude call. The problem: one call means one point of failure, one hard-to-debug black box, and no ability to inspect intermediate outputs. Chaining breaks the work into distinct steps where each step's output feeds the next.

### Core Content

**BriefBot's chained pipeline:**

```
Step 1: Topic Analysis → what do we need to research?
Step 2: Section Planning → what structure should the briefing have?
Step 3: Section Writing → write each section (one call per section)
Step 4: Synthesis → executive summary + key findings
Step 5: Format → assemble final JSON
```

```python
# workflows/chain.py
import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def step_analyze_topic(topic: str) -> dict:
    """Step 1: Understand what kind of research this topic needs."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""
Analyse this research topic and return a JSON object with:
- "category": one of (business, academic, technical, news)
- "key_questions": list of 4 specific questions the briefing should answer
- "likely_complexity": low/medium/high
- "assumption_if_ambiguous": null or a string if you're making an interpretation

Topic: {topic}

Respond with JSON only.
"""
        }]
    )
    return json.loads(response.content[0].text)

def step_plan_sections(topic: str, analysis: dict) -> list[dict]:
    """Step 2: Design the briefing structure based on the topic analysis."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": f"""
Design the section structure for a research briefing.

<topic>{topic}</topic>
<analysis>{json.dumps(analysis)}</analysis>

Return a JSON array of section objects. Each object must have:
- "title": a clear, specific section title
- "focus": one sentence describing what this section covers
- "key_question_addressed": which of the key questions this section answers

Aim for 3–4 sections. Respond with JSON only.
"""
        }]
    )
    return json.loads(response.content[0].text)

def step_write_section(topic: str, section_plan: dict, context: str = "") -> dict:
    """Step 3: Write a single section. Called once per section."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": f"""
Write the following section for a research briefing on: {topic}

Section to write:
- Title: {section_plan['title']}
- Focus: {section_plan['focus']}

{"Additional context from knowledge base:\n" + context if context else ""}

Return a JSON object with:
- "title": the section title (same as above)
- "content": 2–4 paragraphs of well-researched content
- "citations": [] (leave empty for now — citations added in Module 7)

JSON only.
"""
        }]
    )
    return json.loads(response.content[0].text)

def step_synthesize(topic: str, sections: list[dict]) -> dict:
    """Step 4: Generate the executive summary and key findings."""
    sections_text = json.dumps(sections, indent=2)
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": f"""
Given these research sections about "{topic}", generate:
1. An executive_summary (2–3 paragraphs) — should synthesise the whole briefing, not repeat section content verbatim
2. key_findings — exactly 4–6 specific, evidence-based bullet points
3. confidence_level — "high", "medium", or "low" based on evidence quality

<sections>
{sections_text}
</sections>

Return JSON only with keys: executive_summary, key_findings, confidence_level
"""
        }]
    )
    return json.loads(response.content[0].text)

def run_chained_pipeline(topic: str) -> dict:
    """Runs the full chained briefing pipeline."""
    print(f"[Chain] Step 1: Analysing topic...")
    analysis = step_analyze_topic(topic)
    
    print(f"[Chain] Step 2: Planning sections... ({analysis['category']} topic)")
    section_plans = step_plan_sections(topic, analysis)
    
    print(f"[Chain] Step 3: Writing {len(section_plans)} sections...")
    sections = [step_write_section(topic, plan) for plan in section_plans]
    
    print(f"[Chain] Step 4: Synthesising...")
    synthesis = step_synthesize(topic, sections)
    
    return {
        "topic": topic,
        "topic_category": analysis["category"],
        "executive_summary": synthesis["executive_summary"],
        "sections": sections,
        "key_findings": synthesis["key_findings"],
        "confidence_level": synthesis["confidence_level"],
        "sources": [],
        "metadata": {"model": MODEL, "pipeline": "chained"}
    }
```

### Practice Activity
**Eval sprint:** Integrate the chained pipeline into BriefBot and re-run the full eval. Compare against your previous score. Did breaking the task into steps improve output quality? Look at which specific weaknesses the model grader still flags — this tells you where to focus next.

---

## Lesson 4.3 — Routing: Different Topics, Different Pipelines (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

An academic topic about CRISPR gene editing needs different section structure and tone than a business briefing on supply chain disruptions. Routing lets you use a single entry point but diverge to specialised handling based on input.

```python
# workflows/router.py
import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

PIPELINE_CONFIGS = {
    "business": {
        "tone": "analytical and strategic",
        "section_emphasis": ["Market Context", "Key Players", "Risks & Opportunities", "Strategic Outlook"],
        "system_addendum": "Focus on commercial implications, market dynamics, and strategic considerations."
    },
    "academic": {
        "tone": "rigorous and evidence-based",
        "section_emphasis": ["Background", "Current Research", "Methodologies", "Open Questions"],
        "system_addendum": "Emphasise research findings, methodological approaches, and academic consensus vs. debate."
    },
    "technical": {
        "tone": "precise and implementation-focused",
        "section_emphasis": ["Technical Foundation", "Current Approaches", "Limitations", "Emerging Solutions"],
        "system_addendum": "Focus on technical mechanisms, trade-offs between approaches, and practical implementation considerations."
    },
    "news": {
        "tone": "timely and contextual",
        "section_emphasis": ["What Happened", "Why It Matters", "Key Stakeholders", "What Comes Next"],
        "system_addendum": "Emphasise recency, stakeholder perspectives, and near-term implications."
    }
}

def classify_topic(topic: str) -> str:
    """Uses Claude to classify the topic into one of four categories."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""
Classify this research topic into exactly one of: business, academic, technical, news

Topic: {topic}

Respond with the single category word only.
"""
        }]
    )
    category = response.content[0].text.strip().lower()
    return category if category in PIPELINE_CONFIGS else "business"  # Fallback

def route_topic(topic: str) -> tuple[str, dict]:
    """Returns the category and its pipeline configuration."""
    category = classify_topic(topic)
    config = PIPELINE_CONFIGS[category]
    print(f"[Router] Classified '{topic[:40]}...' as: {category}")
    return category, config
```

**Integrating routing into the chained pipeline:**

```python
# workflows/chain.py (updated step_write_section)
def step_write_section(topic: str, section_plan: dict, pipeline_config: dict, context: str = "") -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=f"You write research briefings. Tone: {pipeline_config['tone']}. {pipeline_config['system_addendum']}",
        messages=[{
            "role": "user",
            "content": f"""
Write the section "{section_plan['title']}" for a research briefing on: {topic}
Focus: {section_plan['focus']}
{"Context:\n" + context if context else ""}
Return JSON with: title, content, citations (empty list for now).
"""
        }]
    )
    return json.loads(response.content[0].text)
```

---

## Lesson 4.4 — Parallelization: Research 4 Angles at Once (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Hook

Right now, BriefBot writes sections sequentially — section 1 done, then section 2, then section 3. That's slow. The sections don't depend on each other, so there's no reason they can't be written simultaneously.

### Core Content

**Using `asyncio` for parallel Claude calls**

```python
# workflows/parallel.py
import asyncio
import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL

async_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

async def write_section_async(topic: str, section_plan: dict, pipeline_config: dict) -> dict:
    """Async version of section writing for parallel execution."""
    response = await async_client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=f"Tone: {pipeline_config['tone']}. {pipeline_config['system_addendum']}",
        messages=[{
            "role": "user",
            "content": f"""
Write section "{section_plan['title']}" for: {topic}
Focus: {section_plan['focus']}
Return JSON with: title, content, citations (empty list).
"""
        }]
    )
    return json.loads(response.content[0].text)

async def write_all_sections_parallel(
    topic: str,
    section_plans: list[dict],
    pipeline_config: dict
) -> list[dict]:
    """Writes all sections concurrently. Huge speed improvement for 3+ sections."""
    tasks = [
        write_section_async(topic, plan, pipeline_config)
        for plan in section_plans
    ]
    sections = await asyncio.gather(*tasks)
    return list(sections)

# Call from synchronous code:
def run_sections_parallel(topic, section_plans, pipeline_config):
    return asyncio.run(write_all_sections_parallel(topic, section_plans, pipeline_config))
```

**Speed comparison (approximate, 4 sections):**

| Approach | Time |
|---|---|
| Sequential | ~40–60 seconds |
| Parallel (asyncio) | ~12–18 seconds |

**Error handling in parallel calls**

```python
async def write_section_safe(topic: str, section_plan: dict, pipeline_config: dict) -> dict:
    """Async section writer with fallback on failure."""
    try:
        return await write_section_async(topic, section_plan, pipeline_config)
    except Exception as e:
        print(f"  Warning: Section '{section_plan['title']}' failed: {e}. Using stub.")
        return {
            "title": section_plan["title"],
            "content": f"[Content generation failed for this section. Error: {str(e)[:100]}]",
            "citations": []
        }
```

### Practice Activity
**Benchmark it:** Time the sequential vs. parallel pipeline on the same 3 topics. Record the wall-clock time for each. Then run the eval again — does parallelization affect quality, or just speed?

---

## Module 4 Checkpoint ✅

BriefBot now:
- Chains 5 distinct steps, each independently inspectable
- Routes topics to specialised pipelines based on category
- Writes all sections in parallel, cutting latency by ~70%

---
---

# MODULE 5: Advanced RAG

**Module outcome:** Implement contextual retrieval, hybrid search, and LLM reranking.

**Total time:** ~2.5 hours

---

## Lesson 5.1 — RAG Recap: What You Know, What's Missing (Concept)
**Type:** Concept | **Duration:** 10 min

### Core Content

**What you built in the beginner course:**

1. Chunk documents by size or structure
2. Embed each chunk with Voyage AI
3. Store embeddings in a vector store
4. At query time: embed the user's question, find nearest chunks by cosine similarity
5. Add chunks to Claude's prompt as context

**The three gaps that limit basic RAG:**

1. **Context loss** — When a document is chunked, each chunk loses the context of where it sits in the original document. A chunk about "treatment side effects" doesn't know it came from a section about drug trials vs. a section about home remedies. Without that context, it can be mismatched to the wrong queries.

2. **Semantic search blind spots** — Embedding search finds *meaning* similarity but can miss specific terms. A chunk about "myocardial infarction" might not match a query about "heart attack" as strongly as you'd expect — if the training data didn't strongly link them.

3. **No quality filtering** — You return the top-k chunks by similarity, but "similar" doesn't always mean "relevant." The 3rd and 4th chunks might be close in embedding space but not actually useful for the question.

Modules 5.2 through 5.4 fix all three gaps.

---

## Lesson 5.2 — Contextual Retrieval: Giving Chunks Their Memory Back (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 40 min

### Core Content

**The idea:** Before embedding a chunk, prepend a short AI-generated context description that situates the chunk within the full document. The chunk goes from:

```
"Side effects include nausea, headaches, and in rare cases, elevated liver enzymes."
```

To:

```
"This chunk is from the 'Adverse Effects' section of a 2023 clinical trial report on 
drug X in hypertension patients. Side effects include nausea, headaches, and in rare 
cases, elevated liver enzymes."
```

The embedding of the second version will match far more appropriately to medical queries about that drug's side effects.

**Implementation**

```python
# rag/chunker.py
import anthropic
from config import ANTHROPIC_API_KEY, EVAL_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

CONTEXT_PROMPT = """
Here is a document:
<document>
{document_text}
</document>

Here is a specific chunk from that document:
<chunk>
{chunk_text}
</chunk>

In 2–3 sentences, describe what this chunk is about and where it fits in the overall document.
Be specific about the document's subject and the chunk's role within it.
Write only the context description — no preamble.
"""

def generate_chunk_context(document_text: str, chunk_text: str) -> str:
    """Generates a situating context description for a single chunk."""
    response = client.messages.create(
        model=EVAL_MODEL,  # Use cheaper model for context generation
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": CONTEXT_PROMPT.format(
                document_text=document_text[:3000],  # Truncate for very long docs
                chunk_text=chunk_text
            )
        }]
    )
    return response.content[0].text.strip()

def contextualize_chunks(document_text: str, chunks: list[str]) -> list[str]:
    """
    Takes raw chunks and prepends situating context to each.
    Result: contextualised chunks ready for embedding.
    """
    print(f"Contextualising {len(chunks)} chunks...")
    contextualised = []
    for i, chunk in enumerate(chunks):
        context = generate_chunk_context(document_text, chunk)
        contextualised.append(f"{context}\n\n{chunk}")
        if (i + 1) % 5 == 0:
            print(f"  {i+1}/{len(chunks)} done")
    return contextualised
```

**Cost consideration:** Contextual retrieval runs one LLM call per chunk. For a 50-chunk document, that's 50 API calls upfront — but it's a one-time pre-processing cost. Use prompt caching on the document text to reduce it dramatically (we cover this in Lesson 5.4).

### Practice Activity
**Comparison test:** Embed the same 5 chunks with and without contextualisation. Run a query that requires context awareness (e.g. "What were the adverse events in the trial?"). Compare which version returns more relevant results. Does contextualisation help on your test queries?

---

## Lesson 5.3 — LLM Reranking: Let Claude Pick the Best Chunks (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

**The problem with top-k retrieval**

Vector search returns the k most *similar* chunks. Similar in embedding space doesn't always mean "will actually help answer this question." The 3rd result might embed similarly but be about a tangentially related subtopic.

Reranking adds a second pass: take the top-k candidates, ask Claude to evaluate each one's actual relevance to the query, and reorder based on that judgment.

```python
# rag/retriever.py
import json
import anthropic
from config import ANTHROPIC_API_KEY, EVAL_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

RERANKER_PROMPT = """
You are evaluating whether retrieved document chunks are relevant to a research query.

<query>{query}</query>

Here are the candidate chunks, each with an ID:
<candidates>
{candidates_json}
</candidates>

Return a JSON array of chunk IDs ordered from most relevant to least relevant.
Only include chunks that are actually useful for answering the query.
Discard chunks that are tangentially related or not helpful.

Example format: ["chunk_3", "chunk_1", "chunk_5"]
Respond with JSON only.
"""

def rerank_chunks(query: str, chunks: list[str], top_k: int = 3) -> list[str]:
    """
    Uses Claude to rerank retrieved chunks by actual relevance to the query.
    Returns the top_k most relevant chunks.
    """
    candidates = [
        {"id": f"chunk_{i}", "text": chunk[:500]}  # Truncate for reranker efficiency
        for i, chunk in enumerate(chunks)
    ]
    
    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": RERANKER_PROMPT.format(
                query=query,
                candidates_json=json.dumps(candidates, indent=2)
            )
        }]
    )
    
    ranked_ids = json.loads(response.content[0].text)
    
    # Map IDs back to original chunks, in reranked order
    id_to_chunk = {f"chunk_{i}": chunk for i, chunk in enumerate(chunks)}
    return [id_to_chunk[cid] for cid in ranked_ids[:top_k] if cid in id_to_chunk]

class AdvancedRetriever:
    def __init__(self, vector_store, bm25_store):
        self.vector_store = vector_store
        self.bm25_store = bm25_store
    
    def search(self, query: str, embedder, initial_k: int = 8, final_k: int = 3) -> list[str]:
        """
        Full retrieval pipeline:
        1. Hybrid search (vector + BM25) to get initial candidates
        2. LLM reranking to get the best final_k chunks
        """
        # Step 1: Hybrid retrieval — get more candidates than we need
        query_embedding = embedder.embed(query)
        vector_results = self.vector_store.search(query_embedding, top_k=initial_k // 2)
        bm25_results = self.bm25_store.search(query, top_k=initial_k // 2)
        
        # Deduplicate candidates
        seen = set()
        candidates = []
        for chunk in vector_results + bm25_results:
            if chunk not in seen:
                seen.add(chunk)
                candidates.append(chunk)
        
        # Step 2: LLM reranking
        print(f"  Reranking {len(candidates)} candidates...")
        return rerank_chunks(query, candidates, top_k=final_k)
```

### Practice Activity
**Quality test:** Run the same 10 queries through basic retrieval vs. retrieval with reranking. For each, manually judge: did reranking surface better chunks? What types of queries benefited most from the reranking step?

---

## Lesson 5.4 — Prompt Caching for RAG (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 25 min

### Core Content

**The cost problem with contextual retrieval**

Generating context for 50 chunks means 50 LLM calls. If you also include the full document text in each call (so Claude can situate the chunk), you're sending potentially thousands of tokens of document text 50 times. That's expensive.

Prompt caching solves this: the document text is processed once and cached. Every subsequent chunk context call reads from the cache instead of reprocessing the whole document.

```python
def contextualize_chunks_with_caching(document_text: str, chunks: list[str]) -> list[str]:
    """
    Generates context for all chunks, using prompt caching on the document text.
    The document is only processed once — all chunk calls after the first use the cache.
    """
    contextualised = []
    
    for i, chunk in enumerate(chunks):
        response = client.messages.create(
            model=EVAL_MODEL,
            max_tokens=200,
            system=[{
                "type": "text",
                "text": "You generate concise context descriptions for document chunks.",
                "cache_control": {"type": "ephemeral"}  # Cache the system prompt
            }],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"<document>\n{document_text}\n</document>",
                            "cache_control": {"type": "ephemeral"}  # Cache the document
                        },
                        {
                            "type": "text",
                            "text": f"<chunk>\n{chunk}\n</chunk>\n\nDescribe this chunk's context in 2–3 sentences."
                        }
                    ]
                }
            ]
        )
        
        context = response.content[0].text.strip()
        contextualised.append(f"{context}\n\n{chunk}")
        
        # Log cache behavior for the first few calls
        if i < 3:
            usage = response.usage
            print(f"  Chunk {i+1}: created={usage.cache_creation_input_tokens}, read={usage.cache_read_input_tokens}")
    
    return contextualised
```

**What you'll see in the logs:**
- Chunk 1: `created=1847, read=0` (cache being written)
- Chunk 2: `created=0, read=1847` (cache read — full document processed for free)
- Chunk 3: `created=0, read=1847` (same)

On 50 chunks, this can reduce contextual retrieval cost by 60–80%.

---

## Module 5 Checkpoint ✅

BriefBot's RAG pipeline now:
- Contextualises chunks before embedding (better matches)
- Uses hybrid search + LLM reranking (better quality results)
- Caches documents during contextualisation (dramatically lower cost)

---
---

# MODULE 6: Advanced Tools & Structured Output

**Module outcome:** Implement parallel tool execution; use tool schemas for reliable structured data extraction.

**Total time:** ~2 hours

---

## Lesson 6.1 — Tools for Structured Output: The Reliable Alternative (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 30 min

### Core Content

In the beginner course, you used prefilling + stop sequences to extract JSON. That works — but it has failure modes. Claude might drift away from the prefill, or include extra text before or after the JSON.

There's a more reliable method: define the desired JSON structure as a *tool schema* and force Claude to call it. Since Claude's tool calls are already structured JSON validated against the schema, you get guaranteed valid output.

```python
# tools/schemas.py

EXTRACT_BRIEFING_METADATA_SCHEMA = {
    "name": "save_briefing_metadata",
    "description": """
        Saves the extracted metadata from a research briefing analysis.
        Call this tool with the complete metadata extracted from the briefing content.
        This is the ONLY way to submit your analysis output.
    """,
    "input_schema": {
        "type": "object",
        "properties": {
            "topic_category": {
                "type": "string",
                "enum": ["business", "academic", "technical", "news"],
                "description": "The category of the research topic"
            },
            "key_entities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Main companies, people, technologies, or concepts central to the topic"
            },
            "time_sensitivity": {
                "type": "string",
                "enum": ["evergreen", "months", "weeks", "days"],
                "description": "How quickly this briefing will become outdated"
            },
            "recommended_followup_topics": {
                "type": "array",
                "items": {"type": "string"},
                "description": "2–3 related topics worth researching next"
            }
        },
        "required": ["topic_category", "key_entities", "time_sensitivity", "recommended_followup_topics"]
    }
}
```

```python
# tools/executor.py
import anthropic
from config import ANTHROPIC_API_KEY, MODEL
from tools.schemas import EXTRACT_BRIEFING_METADATA_SCHEMA

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def extract_briefing_metadata(briefing: dict) -> dict:
    """
    Uses a forced tool call to reliably extract structured metadata from a briefing.
    More reliable than prefill + stop sequences for complex nested structures.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        tools=[EXTRACT_BRIEFING_METADATA_SCHEMA],
        tool_choice={"type": "tool", "name": "save_briefing_metadata"},  # Force the call
        messages=[{
            "role": "user",
            "content": f"""
Analyse this research briefing and call save_briefing_metadata with the extracted information.

Topic: {briefing['topic']}
Summary: {briefing['executive_summary'][:500]}
Key findings: {briefing.get('key_findings', [])}
"""
        }]
    )
    
    # The structured data is in the tool call's input — not in response text
    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    return tool_use_block.input  # Already a validated Python dict
```

**When to use this pattern vs. prefilling:**
- Prefilling: simple JSON, few fields, rapid prototyping
- Tool schema: complex nested structures, required fields, production systems, when schema validation matters

---

## Lesson 6.2 — The Batch Tool: Parallel Tool Execution (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

Claude can theoretically send multiple tool use blocks in one message — but in practice it often defaults to sequential tool calls, meaning: call tool A, wait for result, then call tool B. For independent tools, this is unnecessarily slow.

The batch tool is a design pattern that tricks Claude into parallel execution: instead of offering individual tools, you offer a single `batch` tool that accepts a list of tool invocations. Claude calls batch once with all invocations, your code executes them in parallel, and you return all results together.

```python
# tools/schemas.py (add batch schema)
BATCH_TOOL_SCHEMA = {
    "name": "batch_execute",
    "description": """
        Execute multiple independent tool operations simultaneously.
        Use this when you need to call several tools that don't depend on each other's results.
        Pass all desired tool invocations as a list in the 'invocations' parameter.
    """,
    "input_schema": {
        "type": "object",
        "properties": {
            "invocations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tool_name": {"type": "string"},
                        "arguments": {"type": "object"}
                    },
                    "required": ["tool_name", "arguments"]
                },
                "description": "List of tool calls to execute in parallel"
            }
        },
        "required": ["invocations"]
    }
}
```

```python
# tools/executor.py (add batch runner)
import asyncio
import json

AVAILABLE_TOOLS = {
    "search_knowledge_base": lambda args: search_knowledge_base(**args),
    "check_topic_recency": lambda args: check_topic_recency(**args),
    "get_related_topics": lambda args: get_related_topics(**args),
}

async def run_tool_async(tool_name: str, arguments: dict):
    """Async wrapper for tool execution."""
    loop = asyncio.get_event_loop()
    tool_fn = AVAILABLE_TOOLS.get(tool_name)
    if not tool_fn:
        raise ValueError(f"Unknown tool: {tool_name}")
    # Run blocking tool in thread pool to avoid blocking the event loop
    return await loop.run_in_executor(None, lambda: tool_fn(arguments))

async def run_batch_async(invocations: list[dict]) -> list[dict]:
    """Executes all invocations concurrently and returns results in order."""
    tasks = [run_tool_async(inv["tool_name"], inv["arguments"]) for inv in invocations]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    batch_results = []
    for inv, result in zip(invocations, results):
        if isinstance(result, Exception):
            batch_results.append({"tool": inv["tool_name"], "error": str(result)})
        else:
            batch_results.append({"tool": inv["tool_name"], "result": result})
    return batch_results

def handle_batch_tool(invocations: list[dict]) -> str:
    """Synchronous entry point for the batch tool handler."""
    results = asyncio.run(run_batch_async(invocations))
    return json.dumps(results)
```

---

## Lesson 6.3 — Fine-Grained Tool Streaming (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 25 min

### Core Content

When Claude uses tools and you're streaming, there's a default behaviour worth knowing: the API buffers tool argument chunks until a complete, validated JSON key-value pair is ready before sending it to you. This means the stream feels choppy — bursts of content after a pause, not a steady flow.

**Fine-grained mode** disables this validation buffer, sending chunks immediately as they're generated. You get a smoother stream, but you're responsible for handling incomplete JSON gracefully.

```python
import anthropic

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def stream_with_tools(topic: str):
    """Streams a tool-enabled response with fine-grained chunking."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=1000,
        tools=TOOLS,
        betas=["fine-grained-tool-streaming-2025-05-14"],  # Enable fine-grained mode
        messages=[{"role": "user", "content": f"Research this topic: {topic}"}]
    ) as stream:
        for event in stream:
            if hasattr(event, 'type'):
                if event.type == "content_block_delta":
                    if hasattr(event.delta, 'text'):
                        print(event.delta.text, end="", flush=True)
                    elif hasattr(event.delta, 'partial_json'):
                        # Tool argument chunk — may be incomplete JSON
                        # snapshot is the cumulative JSON so far
                        pass  # Handle or buffer as needed
```

**When to use fine-grained mode:**
- Building UI that shows tool argument construction in real-time
- Early processing pipelines that act on partial tool inputs
- Anywhere smooth streaming UX matters more than JSON validation guarantees

---

## Module 6 Checkpoint ✅
BriefBot now extracts structured metadata reliably using tool schemas, and can execute multiple tool calls in parallel using the batch pattern.

---
---

# MODULE 7: Extended Thinking & Citations

**Module outcome:** Enable extended thinking for deep analysis; implement citation linking in briefings.

**Total time:** ~1.5 hours

---

## Lesson 7.1 — Extended Thinking: When Claude Needs to Reason (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

Most Claude tasks benefit from a clear, well-structured prompt. But some tasks — complex trade-off analysis, evaluating conflicting evidence, synthesising ambiguous research — benefit from something more: time to think before committing to an answer.

Extended thinking is exactly that: a separate "thinking phase" where Claude reasons through the problem step by step before writing the final response. You see both the reasoning (in a thinking block) and the conclusion (in the text block).

**When to use it:**
- Complex synthesis where multiple conflicting sources need to be reconciled
- Trade-off analysis with no clear right answer
- Tasks where reasoning transparency matters (auditing, high-stakes decisions)
- When standard prompting produces inconsistent or shallow results despite engineering

**When NOT to use it:**
- Simple factual retrieval — no benefit, just added cost
- High-volume tasks — thinking tokens cost extra and increase latency
- When you've already achieved satisfactory quality through prompt engineering

**For BriefBot:** The synthesis step — where Claude must weigh all research sections and produce an executive summary with genuine insight — is the ideal candidate for extended thinking.

---

## Lesson 7.2 — Implementing Extended Thinking in BriefBot (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

```python
# workflows/chain.py (updated synthesis step)
def step_synthesize_with_thinking(topic: str, sections: list[dict]) -> dict:
    """
    Synthesis step with extended thinking enabled.
    Claude reasons through the findings before writing the executive summary.
    """
    sections_text = json.dumps(sections, indent=2)
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=6000,       # Must exceed thinking_budget
        temperature=1,         # Required when using extended thinking
        thinking={
            "type": "enabled",
            "budget_tokens": 4000  # Tokens Claude can use for thinking
        },
        messages=[{
            "role": "user",
            "content": f"""
You are synthesising a research briefing on: "{topic}"

Here are the research sections:
<sections>
{sections_text}
</sections>

Think carefully about:
- What are the most important and surprising insights across all sections?
- Where do sections agree or conflict?
- What would a knowledgeable analyst conclude that isn't obvious from reading sections individually?
- What confidence level is appropriate given the evidence quality?

Then write:
1. executive_summary: 2–3 paragraphs with genuine analytical insight (not a summary of summaries)
2. key_findings: exactly 5 specific, evidence-based bullets that a decision-maker would care about
3. confidence_level: "high", "medium", or "low" with a one-sentence justification

Return JSON only.
"""
        }]
    )
    
    # Response has multiple blocks: thinking block + text block
    thinking_text = ""
    result_text = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking_text = block.thinking  # Claude's reasoning (for inspection)
        elif block.type == "text":
            result_text = block.text
    
    result = json.loads(result_text)
    result["_thinking_preview"] = thinking_text[:500] + "..."  # Optionally store for debugging
    return result
```

**The thinking block:** You can log `block.thinking` for debugging — it's genuinely interesting to read Claude's reasoning. In production, you'd typically drop it from the final output.

**Redacted thinking blocks:** Occasionally, Claude's thinking touches content the safety system flags, and you receive a `redacted_thinking` block instead. This is intentional — the API continues working, just without that reasoning visible. Your code should handle both:

```python
for block in response.content:
    if block.type == "thinking":
        reasoning = block.thinking
    elif block.type == "redacted_thinking":
        reasoning = "[reasoning redacted by safety system]"
    elif block.type == "text":
        result_text = block.text
```

### Practice Activity
**Eval sprint:** Enable extended thinking only for the synthesis step. Re-run the full eval. Does the executive summary quality improve (per the model grader's scoring of executive_summary depth)? What's the latency increase? Is the quality-to-latency trade-off worth it for your use case?

---

## Lesson 7.3 — Citations: Linking Claims to Sources (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 25 min

### Core Content

The citations API feature lets Claude link specific claims in its responses to passages in source documents, creating a verifiable trail from output to input.

```python
def generate_section_with_citations(topic: str, section_title: str, sources: list[dict]) -> dict:
    """
    Generates a section with citations enabled. Claude will link claims to source passages.
    Each source must have a 'title' and 'content' field.
    """
    # Build source blocks for the message
    source_blocks = []
    for source in sources:
        source_blocks.append({
            "type": "document",
            "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": source["content"]
            },
            "title": source["title"],
            "citations": {"enabled": True}  # Enable citation tracking for this source
        })
    
    source_blocks.append({
        "type": "text",
        "text": f"""
Write the '{section_title}' section for a research briefing on: {topic}

Use information from the provided documents. When you make a specific claim,
cite the source document it comes from.
"""
    })
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": source_blocks
        }]
    )
    
    # Parse the response — citations appear as special content blocks
    text_parts = []
    citations_used = []
    
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
        elif block.type == "citations":
            # Each citation block contains the cited text and source reference
            for citation in block.citations:
                citations_used.append({
                    "source_title": citation.document_title,
                    "quoted_text": citation.cited_text,
                    "start_char": getattr(citation, 'start_char_index', None),
                    "end_char": getattr(citation, 'end_char_index', None)
                })
    
    return {
        "title": section_title,
        "content": " ".join(text_parts),
        "citations": citations_used
    }
```

---

## Module 7 Checkpoint ✅
BriefBot now reasons deeply through synthesis using extended thinking, and links claims to source documents with citations.

---
---

# MODULE 8: Intro to MCP — Model Context Protocol

**Module outcome:** Build a basic MCP server and client; connect BriefBot to external services.

**Total time:** ~2.5 hours

---

## Lesson 8.1 — What MCP Is and Why It Exists (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook

Imagine you want BriefBot to pull data from Notion, post results to Slack, and check your internal knowledge management system. Without MCP, you'd write custom tool schemas and Python functions for every single integration — and maintain them as APIs change.

MCP solves this by standardising how Claude (or any AI model) connects to external services. Instead of writing glue code, you connect to an MCP server — a small, standardised interface around an external service — and the server handles everything.

### Core Content

**The MCP architecture**

```
Your App (MCP Client)
    ↕ (standard protocol)
MCP Server (wraps an external service)
    ↕ (native API calls)
External Service (Notion, GitHub, databases, etc.)
```

**Three things MCP servers expose:**

1. **Tools** — Actions Claude can call (create a document, post a message, run a query)
2. **Resources** — Data Claude can read on-demand (get document contents, list recent files)
3. **Prompts** — Pre-built, tested prompt templates for common tasks with this service

**Who builds MCP servers?** Anyone. Service providers build official ones (Notion, GitHub, AWS have published MCP servers). You can build your own for internal services. The community shares open-source ones.

**MCP vs. writing your own tools:**
- Writing your own: full control, more code, more maintenance
- MCP: standardised, reusable, someone else maintains it, works with any MCP-compatible client

For BriefBot: we'll build a small MCP server that exposes BriefBot's briefing storage, and connect a client to it.

---

## Lesson 8.2 — How MCP Clients and Servers Communicate (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**The communication flow (5 steps):**

```
1. Client → Server: "list_tools" request
2. Server → Client: list of available tool schemas
3. [Claude sees tool list, decides to call one]
4. Client → Server: "call_tool" request (tool name + arguments)
5. Server → Client: tool execution result
```

Both client and server speak a message format defined by the MCP specification. The transport layer (how bytes move between them) can be stdio (standard input/output, both on same machine), HTTP, or WebSockets.

For our purposes: we'll use stdio — the simplest setup, client and server running on the same machine.

**Install the MCP Python SDK:**

```bash
pip install mcp
```

---

## Lesson 8.3 — Building Your First MCP Server (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

We'll build a BriefBot Storage Server — an MCP server that stores and retrieves briefings.

```python
# mcp_server/server.py
import json
import asyncio
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from pydantic import Field

# In-memory briefing store (would be a database in production)
briefing_store: dict[str, dict] = {}

server = Server("briefbot-storage")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="save_briefing",
            description="Save a research briefing to the BriefBot storage system. Use this after generating a briefing to persist it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "briefing_id": {
                        "type": "string",
                        "description": "Unique identifier for this briefing (e.g. topic slug)"
                    },
                    "briefing_data": {
                        "type": "object",
                        "description": "The full briefing data dict to store"
                    }
                },
                "required": ["briefing_id", "briefing_data"]
            }
        ),
        types.Tool(
            name="get_briefing",
            description="Retrieve a previously saved briefing by its ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "briefing_id": {
                        "type": "string",
                        "description": "The ID of the briefing to retrieve"
                    }
                },
                "required": ["briefing_id"]
            }
        ),
        types.Tool(
            name="list_briefings",
            description="List all saved briefing IDs with their topics and creation times.",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "save_briefing":
        briefing_id = arguments["briefing_id"]
        briefing_store[briefing_id] = {
            **arguments["briefing_data"],
            "saved_at": datetime.now().isoformat()
        }
        return [types.TextContent(type="text", text=f"Briefing '{briefing_id}' saved successfully.")]
    
    elif name == "get_briefing":
        briefing_id = arguments["briefing_id"]
        if briefing_id not in briefing_store:
            return [types.TextContent(type="text", text=f"No briefing found with ID '{briefing_id}'.")]
        return [types.TextContent(type="text", text=json.dumps(briefing_store[briefing_id]))]
    
    elif name == "list_briefings":
        if not briefing_store:
            return [types.TextContent(type="text", text="No briefings saved yet.")]
        summary = [
            {"id": bid, "topic": b.get("topic", "Unknown"), "saved_at": b.get("saved_at")}
            for bid, b in briefing_store.items()
        ]
        return [types.TextContent(type="text", text=json.dumps(summary, indent=2))]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**Testing with the MCP Inspector:**

```bash
mcp dev mcp_server/server.py
```

This opens an in-browser debugger. Navigate to Tools → `list_briefings` → click Run. Then test `save_briefing` by filling in a briefing ID and a sample JSON object. Verify the saved briefing appears in `list_briefings`.

---

## Lesson 8.4 — Building the MCP Client (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

```python
# mcp_client/client.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class BriefBotStorageClient:
    """MCP client for connecting to the BriefBot storage server."""
    
    def __init__(self):
        self.session = None
        self._context = None
    
    async def __aenter__(self):
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server/server.py"]
        )
        self._context = stdio_client(server_params)
        read_stream, write_stream = await self._context.__aenter__()
        self.session = ClientSession(read_stream, write_stream)
        await self.session.__aenter__()
        await self.session.initialize()
        return self
    
    async def __aexit__(self, *args):
        await self.session.__aexit__(*args)
        await self._context.__aexit__(*args)
    
    async def list_tools(self) -> list:
        result = await self.session.list_tools()
        return result.tools
    
    async def save_briefing(self, briefing_id: str, briefing: dict) -> str:
        result = await self.session.call_tool(
            "save_briefing",
            {"briefing_id": briefing_id, "briefing_data": briefing}
        )
        return result.content[0].text
    
    async def get_briefing(self, briefing_id: str) -> dict | None:
        result = await self.session.call_tool(
            "get_briefing",
            {"briefing_id": briefing_id}
        )
        text = result.content[0].text
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None  # "No briefing found" message
    
    async def list_briefings(self) -> list:
        result = await self.session.call_tool("list_briefings", {})
        return json.loads(result.content[0].text)

# Usage example:
async def demo():
    async with BriefBotStorageClient() as client:
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # Save a briefing
        fake_briefing = {"topic": "Solar energy", "executive_summary": "..."}
        msg = await client.save_briefing("solar-energy-2026", fake_briefing)
        print(msg)
        
        # Retrieve it
        retrieved = await client.get_briefing("solar-energy-2026")
        print(f"Retrieved: {retrieved['topic']}")

asyncio.run(demo())
```

---

## Lesson 8.5 — MCP Resources and Prompts (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 25 min

### Core Content

**Resources — data access without tool calls**

Resources let the MCP server expose data that a client can fetch directly, without going through Claude. Useful for reading current state of the system.

```python
# In server.py — add resource support
from mcp.server import Server
from mcp import types

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="briefbot://briefings",
            name="All Briefings",
            description="List of all saved briefings",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if str(uri) == "briefbot://briefings":
        return json.dumps(list(briefing_store.keys()))
    raise ValueError(f"Unknown resource: {uri}")
```

**Prompts — reusable templates server authors test and maintain**

```python
@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="summarise_briefing",
            description="Summarise an existing briefing in plain language for a non-expert audience",
            arguments=[
                types.PromptArgument(
                    name="briefing_id",
                    description="The ID of the briefing to summarise",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    if name == "summarise_briefing":
        briefing_id = arguments["briefing_id"]
        briefing = briefing_store.get(briefing_id, {})
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"""
Please read briefing '{briefing_id}' using the get_briefing tool, 
then write a plain-language 3-paragraph summary suitable for a non-expert reader.
Focus on practical implications rather than technical details.
Briefing topic: {briefing.get('topic', 'Unknown')}
"""
                    )
                )
            ]
        )
```

---

## Module 8 Checkpoint ✅
BriefBot now has a working MCP server (tools + resources + prompts) and a Python client that connects to it. The groundwork is laid for connecting Claude to external systems in the Advanced course.

---
---

# MODULE 9: Final Assembly + What Comes Next

**Module outcome:** Assemble complete BriefBot; understand what the Advanced course covers.

**Total time:** ~1.5 hours

---

## Lesson 9.1 — Files API + Code Execution (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 30 min

### Core Content

Two powerful API features we haven't covered — worth knowing before you finish:

**Files API** — Upload a file once, reference it by ID in future requests. Instead of base64-encoding the same PDF in every request, upload it once and pass the file ID. Useful for BriefBot when you have a static knowledge base of PDFs.

```python
# Upload a document once
with open("knowledge_base/report.pdf", "rb") as f:
    file_obj = client.beta.files.upload(
        file=("report.pdf", f, "application/pdf")
    )
file_id = file_obj.id  # e.g. "file-abc123"

# Reference by ID in future requests (no re-uploading)
response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "file",
                    "file_id": file_id  # Reference, not bytes
                }
            },
            {"type": "text", "text": "Summarise the key findings from this report."}
        ]
    }],
    betas=["files-api-2025-04-14"]
)
```

**Code Execution** — Claude runs Python code in an isolated Docker container, interprets the results, and responds. No implementation needed — just include the tool schema.

```python
CODE_EXECUTION_TOOL = {
    "type": "computer_use_20250124",  # Schema type for code execution
    "name": "code_execution"
}
```

BriefBot application: Ask Claude to generate charts or statistical summaries from data in the knowledge base, and get the image files back.

---

## Lesson 9.2 — BriefBot Final Assembly (Workshop)
**Type:** Workshop | **Duration:** 45 min

### Core Content

The complete BriefBot pipeline, fully assembled:

```python
# briefbot.py — final version
class BriefBot:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.retriever = AdvancedRetriever(vector_store, bm25_store)
        self.mcp_client = BriefBotStorageClient()
    
    async def generate_briefing(self, topic: str, save: bool = True) -> dict:
        """Full BriefBot pipeline."""
        
        # 1. Route topic
        category, pipeline_config = route_topic(topic)
        
        # 2. Plan sections (chained)
        analysis = step_analyze_topic(topic)
        section_plans = step_plan_sections(topic, analysis)
        
        # 3. RAG: get relevant knowledge base chunks
        rag_context = self.retriever.search(topic, embedder)
        rag_text = "\n\n---\n\n".join(rag_context)
        
        # 4. Write sections in parallel (with RAG context)
        sections = await write_all_sections_parallel(topic, section_plans, pipeline_config, context=rag_text)
        
        # 5. Synthesise with extended thinking
        synthesis = step_synthesize_with_thinking(topic, sections)
        
        # 6. Extract metadata with tool schema
        metadata = extract_briefing_metadata({**synthesis, "sections": sections})
        
        briefing = {
            "topic": topic,
            "topic_category": category,
            "executive_summary": synthesis["executive_summary"],
            "sections": sections,
            "key_findings": synthesis["key_findings"],
            "confidence_level": synthesis["confidence_level"],
            "sources": [],
            "metadata": {
                "model": MODEL,
                "pipeline": "full_v2",
                **metadata
            }
        }
        
        # 7. Save via MCP
        if save:
            async with BriefBotStorageClient() as mcp:
                briefing_id = topic.lower().replace(" ", "-")[:50]
                await mcp.save_briefing(briefing_id, briefing)
        
        return briefing
```

**Final eval run:** Run the complete eval with the full pipeline. Record your final score and compare the improvement journey from your baseline.

---

## Lesson 9.3 — Production Checklist + Advanced Preview (Concept)
**Type:** Concept | **Duration:** 20 min

### Production Checklist for BriefBot

Before calling any AI system "production-ready":

**Reliability**
- [ ] Eval pipeline with >20 test cases, consistent score ≥ 7.5
- [ ] All tool calls have try/except with graceful failure handling
- [ ] Retry logic for transient API failures (use `tenacity` library)
- [ ] Max_iterations cap on the evaluator-optimizer loop

**Cost & Latency**
- [ ] Prompt caching enabled for system prompts and large static content
- [ ] Parallelization used wherever steps are independent
- [ ] Appropriate model choice per task (Haiku for grading, Sonnet for generation)

**Observability**
- [ ] Token usage logged per request
- [ ] Latency tracked per pipeline step
- [ ] Eval score stored alongside every generated briefing

**Safety**
- [ ] No raw user input directly interpolated without sanitisation
- [ ] API keys in environment variables, never in code
- [ ] Rate limiting considered for high-volume scenarios

---

### What the Advanced Course Covers (Course 3 of 3)

You've gone from "it works" to "it works reliably." The Advanced course takes you to "it works at scale, autonomously, with minimal supervision."

**Advanced Course Preview:**
- **Deep MCP** — Building and deploying production MCP servers; connecting to official third-party MCP servers (GitHub, Notion, AWS); multi-server architectures
- **Multi-agent systems** — Orchestrator + specialist agent patterns; agent communication; parallelizing agents across tasks
- **Claude Code in depth** — Custom commands, work trees for parallel development, automated debugging pipelines, CI/CD integration
- **Computer Use** — The tool system behind it, Docker setup, building your own computer use applications
- **Advanced agents** — Environment inspection, self-correcting agent loops, building agents that test their own outputs
- **Production architecture** — Rate limits, batching, async at scale, cost optimisation at volume

---

## Final Project: BriefBot Variant

**The challenge:** Build a BriefBot variant for a domain of your choice. Examples:
- **Legal Briefer** — summarises regulatory changes with citations to official documents
- **Market Intel** — daily competitor briefings routed by industry
- **Research Synthesiser** — academic literature summaries with confidence levels

**Requirements:**
- ✅ Eval pipeline with ≥15 test cases and baseline + final scores documented
- ✅ Chaining workflow with ≥3 distinct steps
- ✅ Routing based on input classification
- ✅ Parallelization for at least one step
- ✅ Advanced RAG (contextual retrieval + reranking)
- ✅ Extended thinking on at least one step
- ✅ Structured output via tool schema
- ✅ Working MCP server with ≥2 tools

---

## Final Project Rubric

| Criterion (25% each) | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|---|---|---|---|---|
| **Eval pipeline** | ≥15 cases, both grader types, score ≥7.5, before/after documented | ≥10 cases, both grader types, score ≥6 | ≥5 cases, one grader type | Fewer than 5 cases or grader missing |
| **Workflow architecture** | All 3 patterns implemented, clearly distinct, error handling throughout | 2 of 3 patterns implemented, basic error handling | 1 pattern implemented | Single monolithic call |
| **RAG quality** | Contextual retrieval + reranking + caching all present; retrieval visibly improves output | Contextual retrieval + one of reranking/caching | Basic hybrid search only | Single-index semantic only |
| **Production features** | Extended thinking + citations + tool schema extraction + MCP integration all present | 3 of 4 production features | 2 of 4 production features | Fewer than 2 |

---

---

# Appendix: Assessment Plan

| Assessment | After | Type | Outcomes | Est. Time |
|---|---|---|---|---|
| Module 1–2 Quiz | Module 2 | 10 MCQ | 1 | 15 min |
| Assignment 1: Grader Design | Module 2 | Code + written | 1 | 2 hrs |
| Module 3–4 Quiz | Module 4 | 10 MCQ + 2 short answer | 2, 3 | 25 min |
| Assignment 2: Workflow Comparison | Module 4 | Code + analysis | 2 | 3 hrs |
| Module 5–6 Quiz | Module 6 | 10 MCQ | 4, 5 | 15 min |
| Assignment 3: RAG Quality Analysis | Module 5 | Code + eval report | 4 | 2.5 hrs |
| Module 7–8 Quiz | Module 8 | 10 MCQ | 6, 7 | 15 min |
| Final Project | Full course | Build | 1–7 | 8–12 hrs |

---

## Module Quiz Topics

**Module 1–2:** Why eval pipelines over manual testing; code grader vs model grader trade-offs; what the average eval score tells you; why reasoning before score matters; combining grader types

**Module 3–4:** Evaluator-optimizer loop mechanics; when to use workflows vs agents; why chaining improves debuggability; parallelization with asyncio; routing classification failure modes

**Module 5–6:** Three gaps in basic RAG; contextual retrieval purpose and cost; what reranking adds vs. initial retrieval; when to use tool schema extraction vs. prefilling; batch tool design pattern

**Module 7–8:** When to enable extended thinking; what redacted thinking blocks mean; citations API response structure; MCP transport options; three things MCP servers expose; difference between resources and tools

---

## Notes for Course Expansion

- Module 2 (Eval) can be expanded significantly with a live eval dashboard using Streamlit or a simple HTML report
- Module 4 (Workflows) pairs well with a system design exercise where learners diagram BriefBot's architecture before coding it
- Module 5 (Advanced RAG) could include a dedicated section on chunking strategy selection for different document types
- Module 8 (MCP) can be expanded to cover connecting to official third-party MCP servers (e.g. running the official GitHub MCP server locally)
- Consider adding an async patterns primer lesson before Module 4 for learners who are less confident with asyncio
- The evaluator-optimizer loop in Module 3 is worth a case study lesson showing real score trajectories across 5 iterations
