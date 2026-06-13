# Architect Production AI Systems with the Claude API
## Series 3 of 3 — Advanced

> **Prerequisite:** Intermediate Claude API Course (you can build eval pipelines, multi-step workflows, advanced RAG, basic MCP, and extended thinking)
> **Format:** Self-paced | **Duration:** 18–22 hours | **Skill Level:** Advanced — production-minded developers

---

## How This Course Is Different From the Intermediate Course

Intermediate taught you to build AI systems that work *reliably*. Advanced teaches you to build AI systems that work reliably **at scale, autonomously, with multiple agents coordinating, across real external services, in production**.

The shift:

| Intermediate thinking | Advanced thinking |
|---|---|
| One BriefBot with a good eval score | A fleet of agents running 1,000 jobs/day |
| "It works on my machine" | "It recovers when the API goes down at 3am" |
| I write tool schemas by hand | I build MCP servers that *other tools* connect to |
| Claude does one thing well | Orchestrator delegates to specialist agents who debate each other |
| I log errors manually | I have a dashboard tracking cost, latency, and quality in real time |
| I know what Claude will do next | I've designed state machines that handle 12 possible agent paths |

This is the course where AI engineering meets systems engineering.

---

## The Single Project: ContentForge — AI Content Operations Engine

**ContentForge** is a production-grade multi-agent content pipeline. You give it a content brief, and it autonomously researches, drafts, debates quality, revises, gets human approval, publishes across platforms, and verifies the result — while tracking every token, dollar, and latency millisecond.

**What ContentForge does end-to-end:**

```
Content Brief
      ↓
[Orchestrator Agent] — plans strategy, delegates tasks, manages state
      ↓
[Researcher Agents × N] — run in parallel, gather from multiple sources
      ↓
[Writer Agent] — drafts full content piece
      ↓
[Editor ⟺ Critic Agent Debate] — challenge and refine quality
      ↓
[Writer Self-Corrects] — revises based on debate findings
      ↓
[Human-in-the-Loop Gate] — approval before publish
      ↓
[Publisher Agent] — distributes via MCP to GitHub / Notion / Slack
      ↓
[Computer Use Agent] — verifies rendered content in browser
      ↓
Structured output + observability metrics + cost report
```

**What a ContentForge job object looks like:**

```json
{
  "job_id": "job_8f3a2c",
  "status": "published",
  "brief": {
    "topic": "How async Python improves AI pipeline throughput",
    "audience": "senior engineers",
    "format": "technical blog post",
    "platforms": ["github", "notion"]
  },
  "agent_trace": [
    {"agent": "orchestrator", "action": "plan", "duration_s": 3.2},
    {"agent": "researcher_1", "action": "web_search", "duration_s": 8.1},
    {"agent": "researcher_2", "action": "kb_search", "duration_s": 4.7},
    {"agent": "writer", "action": "draft", "duration_s": 12.4},
    {"agent": "editor", "action": "critique", "duration_s": 5.9},
    {"agent": "critic", "action": "debate", "duration_s": 4.2},
    {"agent": "writer", "action": "revise", "duration_s": 9.1},
    {"agent": "human", "action": "approved", "duration_s": 0},
    {"agent": "publisher", "action": "publish_github", "duration_s": 2.3},
    {"agent": "computer_use", "action": "verify_render", "duration_s": 15.6}
  ],
  "final_content": { "title": "...", "body": "...", "word_count": 1240 },
  "published_locations": [
    {"platform": "github", "url": "https://github.com/org/repo/blob/main/posts/async-python.md"},
    {"platform": "notion", "url": "https://notion.so/page/abc123"}
  ],
  "metrics": {
    "total_cost_usd": 0.31,
    "total_tokens": 18420,
    "total_latency_s": 65.5,
    "debate_rounds": 1,
    "revision_cycles": 2,
    "quality_score": 8.4
  }
}
```

**Why this project exercises every pillar:**

| Pillar | Where ContentForge uses it |
|--------|---------------------------|
| Multi-agent | Orchestrator + 4 specialists + debate + HITL + memory |
| Production Scale | Async queues, rate limits, cost tracking, circuit breakers |
| Deep MCP | Custom ContentForge MCP server + GitHub + Notion + Slack |
| Claude Code | ContentForge spawns Claude Code to write code content |
| Computer Use | Browser agent verifies published posts render correctly |

---

## Learner Persona

**Name:** Tariq — The Production Engineer

**Who he is:** A developer who has shipped at least one AI feature in a real product. He has real eval pipelines, real tool use implementations, and probably a real BriefBot variant running somewhere. He's hit real problems — API timeouts at peak traffic, a prompt that mysteriously degraded after a month, a tool call that silently failed. He's ready to stop patching and start architecting.

**What he knows:** All of Courses 1 and 2. Comfortable with async Python, basic distributed systems concepts (queues, workers), and has at least heard of Celery, Docker, and structured logging.

**What he wants:** The patterns and code that real AI engineering teams use — not tutorials, but blueprints.

**The gap:** He's never built multi-agent systems with coordination protocols. His production monitoring is still `print()` statements and crossed fingers. He knows MCP exists but hasn't deployed one externally.

**Success looks like:** Tariq ships ContentForge as a real internal tool, runs it at 500+ jobs/week, and presents it to his team with a live observability dashboard showing cost and quality metrics.

---

## Course-Level Learning Outcomes

By the end of this course, learners will be able to:

1. **Design** multi-agent systems using orchestrator-worker, debate, parallel, self-correcting, HITL, and memory patterns
2. **Build** production MCP servers with authentication and versioning, and connect to third-party MCP services
3. **Implement** async task queues and rate-limit-aware pipelines that handle 1,000+ AI requests per day
4. **Instrument** AI systems with structured observability — token usage, latency, cost per job, quality score tracking
5. **Engineer** resilient AI pipelines with retry logic, circuit breakers, and production quality drift detection
6. **Orchestrate** Claude Code programmatically as an autonomous agent within larger AI pipelines
7. **Build** Computer Use applications that interact with real browser interfaces for automated verification

---

## Module Map

| # | Module | Primary Pillar | ContentForge Milestone | Est. Time |
|---|--------|----------------|------------------------|-----------|
| 1 | Architecture & System Design | — | ContentForge skeleton + agent interfaces | 1.5 hrs |
| 2 | Orchestrator-Worker & Parallel Agents | Multi-Agent | Orchestrator delegates; researchers run in parallel | 2.5 hrs |
| 3 | Agent Debate, Self-Correction & Memory | Multi-Agent | Writer/Editor debate; agent remembers brand voice | 2.5 hrs |
| 4 | Human-in-the-Loop & Agent State Machines | Multi-Agent | HITL approval gate; full agent coordination flow | 1.5 hrs |
| 5 | Deep MCP: Production Servers | MCP | ContentForge's own authenticated MCP server deployed | 2.5 hrs |
| 6 | Deep MCP: Third-Party Integrations | MCP | GitHub + Notion + Slack connected; multi-server routing | 2 hrs |
| 7 | Async Pipelines & Task Queues at Scale | Production | Celery queue; 1,000+ req/day without crashes | 2 hrs |
| 8 | Observability, Cost Control & Rate Limiting | Production | Real-time dashboard; token + cost + latency tracking | 2.5 hrs |
| 9 | Resilience & Quality Monitoring | Production | Circuit breakers; drift detection; score alerting | 1.5 hrs |
| 10 | Claude Code as an Orchestrated Agent | Claude Code | ContentForge spawns Claude Code for code content | 1.5 hrs |
| 11 | Computer Use: Real Browser Automation | Computer Use | Browser agent verifies published content renders correctly | 2 hrs |

**Total: ~22 hours**

---
---

# MODULE 1: Architecture & System Design

**Module outcome:** Design ContentForge's agent architecture; establish base classes and interfaces; understand what production-grade AI system design looks like before writing a line of agent code.

**Total time:** ~1.5 hours

---

## Lesson 1.1 — Systems Thinking for AI Engineers (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook

Here's what distinguishes a senior AI engineer from a capable one: the senior engineer designs the *failure modes* before writing the happy path. They ask: what happens when the writer agent produces garbage on the 200th job? What happens when the Notion API goes down mid-publish? What happens when the user never clicks "approve"?

Advanced AI engineering is 30% building the system and 70% designing it to survive real conditions. This module is about the 70%.

### Core Content

**The six design questions to answer before writing agent code:**

1. **What is the unit of work?** For ContentForge, it's a *job* — one content brief → one published piece. Every design decision should serve job completion.

2. **What can fail independently?** Each agent, each MCP connection, each external API. Draw a dependency graph. Anything with an external dependency needs a failure strategy.

3. **What needs human judgment?** Don't automate approval that humans should own. Define your human-in-the-loop gates explicitly.

4. **What state needs to persist?** If ContentForge crashes mid-job, what must survive? Job state, agent memory, partial outputs.

5. **What will you measure?** Design observability before you need it. You cannot debug a black box running 1,000 jobs/day.

6. **What's the coordination protocol?** How do agents communicate? Shared state? Message passing? Event bus? Define this upfront or you'll refactor it later.

**ContentForge's answers:**

| Question | ContentForge's answer |
|---|---|
| Unit of work | ContentJob — a Pydantic model with full job lifecycle |
| Can fail independently | Each agent, each MCP server, web search API |
| Needs human judgment | The approval gate between revision and publishing |
| State that must persist | Job status, agent outputs, debate transcript, approval state |
| What we measure | Tokens per agent, cost per job, latency per step, quality score |
| Coordination protocol | Orchestrator owns state; agents return structured output; message passing via task queue |

---

## Lesson 1.2 — ContentForge Architecture Deep Dive (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 30 min

### Core Content

**Project structure:**

```
contentforge/
├── main.py
├── config.py
├── models/
│   ├── job.py           # ContentJob Pydantic model
│   └── agent_output.py  # Structured agent outputs
├── agents/
│   ├── base.py          # BaseAgent class all agents inherit
│   ├── orchestrator.py  # Plans, delegates, manages state
│   ├── researcher.py    # Web + knowledge base search
│   ├── writer.py        # Content drafting + revision
│   ├── editor.py        # Quality critique
│   ├── critic.py        # Debate partner for editor
│   └── publisher.py     # MCP-based distribution
├── mcp/
│   ├── server/          # ContentForge's own MCP server
│   └── clients/         # Third-party MCP clients (GitHub, Notion, Slack)
├── queue/
│   ├── worker.py        # Celery worker
│   └── tasks.py         # Celery task definitions
├── observability/
│   ├── logger.py        # Structured logging
│   ├── metrics.py       # Cost, token, latency tracking
│   └── dashboard.py     # Real-time monitoring
├── memory/
│   └── agent_memory.py  # Cross-session agent memory
└── computer_use/
    └── verifier.py      # Browser verification agent
```

**The ContentJob model — the spine of the whole system:**

```python
# models/job.py
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
import uuid

class JobStatus(str, Enum):
    PENDING = "pending"
    RESEARCHING = "researching"
    DRAFTING = "drafting"
    IN_DEBATE = "in_debate"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    PUBLISHING = "publishing"
    VERIFYING = "verifying"
    PUBLISHED = "published"
    FAILED = "failed"

class ContentBrief(BaseModel):
    topic: str
    audience: str
    format: str  # blog_post, newsletter, technical_doc, social_post
    platforms: list[str]  # github, notion, slack
    tone: str = "professional"
    word_count_target: int = 800
    brand_context: Optional[str] = None

class AgentTrace(BaseModel):
    agent: str
    action: str
    started_at: datetime
    duration_s: float
    tokens_used: int = 0
    cost_usd: float = 0.0
    output_preview: Optional[str] = None
    error: Optional[str] = None

class ContentJob(BaseModel):
    job_id: str = Field(default_factory=lambda: f"job_{uuid.uuid4().hex[:8]}")
    status: JobStatus = JobStatus.PENDING
    brief: ContentBrief
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Agent outputs (populated progressively)
    research_findings: list[dict] = []
    draft_content: Optional[dict] = None
    debate_transcript: list[dict] = []
    final_content: Optional[dict] = None
    
    # Approval
    approval_status: Optional[str] = None
    approved_by: Optional[str] = None
    
    # Publishing
    published_locations: list[dict] = []
    verification_result: Optional[dict] = None
    
    # Observability
    agent_trace: list[AgentTrace] = []
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    quality_score: Optional[float] = None
    
    def update_status(self, new_status: JobStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.now()
    
    def add_trace(self, trace: AgentTrace) -> None:
        self.agent_trace.append(trace)
        self.total_cost_usd += trace.cost_usd
        self.total_tokens += trace.tokens_used
```

**The BaseAgent — every agent inherits this:**

```python
# agents/base.py
import time
from abc import ABC, abstractmethod
from datetime import datetime
import anthropic
from config import ANTHROPIC_API_KEY, MODEL
from models.job import ContentJob, AgentTrace
from observability.logger import get_logger
from observability.metrics import record_agent_call

logger = get_logger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = MODEL
    
    @abstractmethod
    async def run(self, job: ContentJob) -> dict:
        """Execute this agent's task. Returns structured output."""
        pass
    
    async def execute(self, job: ContentJob) -> dict:
        """
        Wrapper around run() that handles tracing, timing, and error recording.
        All agents call execute(), not run() directly.
        """
        start = time.time()
        started_at = datetime.now()
        
        logger.info(f"Agent '{self.name}' starting", job_id=job.job_id)
        
        try:
            output = await self.run(job)
            duration = time.time() - start
            
            # Record trace
            tokens = output.get("_tokens_used", 0)
            cost = tokens * 0.000003  # Approximate Sonnet cost
            
            trace = AgentTrace(
                agent=self.name,
                action=output.get("_action", "run"),
                started_at=started_at,
                duration_s=round(duration, 2),
                tokens_used=tokens,
                cost_usd=round(cost, 6),
                output_preview=str(output.get("_preview", ""))[:100]
            )
            job.add_trace(trace)
            
            # Record metrics
            record_agent_call(self.name, duration, tokens, cost, success=True)
            
            logger.info(f"Agent '{self.name}' completed", 
                       job_id=job.job_id, duration_s=duration, tokens=tokens)
            return output
        
        except Exception as e:
            duration = time.time() - start
            trace = AgentTrace(
                agent=self.name,
                action="error",
                started_at=started_at,
                duration_s=round(duration, 2),
                error=str(e)
            )
            job.add_trace(trace)
            record_agent_call(self.name, duration, 0, 0, success=False)
            logger.error(f"Agent '{self.name}' failed", job_id=job.job_id, error=str(e))
            raise
```

### Practice Activity
**Setup task:** Create the full folder structure, implement `ContentJob` and `BaseAgent`, write a `StubAgent` that inherits `BaseAgent` and returns a hardcoded output. Confirm the trace is recorded and the job's `total_cost_usd` updates correctly.

---

## Lesson 1.3 — Configuration for Production Systems (Demo)
**Type:** Demo | **Duration:** 20 min

### Core Content

Production systems have more configuration than tutorials show. Here's ContentForge's full config:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

# Model Selection per task
MODEL = "claude-sonnet-4-6"          # Main agents
EVAL_MODEL = "claude-haiku-4-5-20251001" # Grading, classification (cheaper)
ORCHESTRATOR_MODEL = "claude-opus-4-6"   # Orchestrator gets the best model

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 50
MAX_TOKENS_PER_MINUTE = 100_000
RETRY_MAX_ATTEMPTS = 3
RETRY_BASE_DELAY = 1.0  # seconds
RETRY_MAX_DELAY = 60.0

# Cost Guardrails
MAX_COST_PER_JOB_USD = 2.00   # Kill job if it exceeds this
DAILY_BUDGET_USD = 50.00       # Alert if daily spend approaches this

# Quality Thresholds
MIN_QUALITY_SCORE = 6.5        # Jobs below this trigger auto-revision
QUALITY_DRIFT_ALERT = 0.8      # Alert if 7-day avg drops by 0.8 points

# Task Queue
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MAX_CONCURRENT_JOBS = 10
JOB_TIMEOUT_SECONDS = 300

# MCP Servers
MCP_SERVER_HOST = os.getenv("MCP_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_PORT", "8080"))
MCP_AUTH_SECRET = os.getenv("MCP_AUTH_SECRET")

# External MCP URLs
GITHUB_MCP_URL = os.getenv("GITHUB_MCP_URL")
NOTION_MCP_URL = os.getenv("NOTION_MCP_URL")
SLACK_MCP_URL = os.getenv("SLACK_MCP_URL")
```

### Module 1 Checkpoint ✅
ContentForge skeleton is live. Job model, base agent, and production configuration are in place.

---
---

# MODULE 2: Orchestrator-Worker & Parallel Agents

**Module outcome:** Build the Orchestrator agent that delegates tasks; run Researcher agents in true parallel.

**Total time:** ~2.5 hours

---

## Lesson 2.1 — The Orchestrator Pattern (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

The orchestrator is the only agent that knows the full picture. Specialist agents know only their job. The orchestrator:
- Holds the job state
- Decides what runs next and when
- Handles agent failures (retry? skip? escalate?)
- Enforces the overall workflow sequence

**Why not just have one agent do everything?** Three reasons:

1. **Focus** — A writer agent with a single job (write well) outperforms an agent asked to also plan, research, and publish simultaneously.

2. **Fault isolation** — When the researcher fails, it fails cleanly. The orchestrator decides whether to retry, use partial results, or abort. The writer never sees the failure.

3. **Observability** — Every agent handoff is a measurable event. You know exactly where time and money are being spent.

**The orchestrator's decision loop:**

```
[Receive job]
      ↓
[Plan: decide which agents to run and in what order]
      ↓
[Dispatch: send tasks to agents]
      ↓
[Monitor: wait for outputs, handle failures]
      ↓
[Gate: should we proceed to next stage?]
      ↓
[Repeat until job is complete or aborted]
```

---

## Lesson 2.2 — Building the ContentForge Orchestrator (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

```python
# agents/orchestrator.py
import asyncio
import json
from agents.base import BaseAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.editor import EditorAgent
from agents.publisher import PublisherAgent
from models.job import ContentJob, JobStatus
from config import ORCHESTRATOR_MODEL, MAX_COST_PER_JOB_USD

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("orchestrator")
        self.model = ORCHESTRATOR_MODEL  # Best model for planning decisions
    
    async def run(self, job: ContentJob) -> dict:
        """
        Plans the content strategy and returns a structured execution plan.
        The plan tells us: how many researchers, what angles, what format priorities.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": f"""
You are orchestrating a content production pipeline.

<brief>
Topic: {job.brief.topic}
Audience: {job.brief.audience}
Format: {job.brief.format}
Target word count: {job.brief.word_count_target}
Platforms: {', '.join(job.brief.platforms)}
Tone: {job.brief.tone}
</brief>

Plan the research strategy. Return JSON with:
- "research_angles": list of 3 specific research angles to pursue in parallel
- "section_structure": list of section titles for the final piece  
- "key_emphasis": what this audience cares most about
- "potential_pitfalls": what common errors to avoid for this topic/audience combo
- "estimated_complexity": low/medium/high

JSON only.
"""
            }]
        )
        
        plan = json.loads(response.content[0].text)
        
        return {
            "_action": "plan",
            "_tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "_preview": f"Plan: {len(plan['research_angles'])} research angles",
            "plan": plan
        }
    
    async def run_full_pipeline(self, job: ContentJob) -> ContentJob:
        """
        Runs the complete ContentForge pipeline from brief to published.
        This is the main entry point called by the task queue.
        """
        try:
            # Stage 1: Plan
            job.update_status(JobStatus.RESEARCHING)
            plan_output = await self.execute(job)
            plan = plan_output["plan"]
            
            # Cost guardrail — check before each expensive stage
            self._check_cost_limit(job)
            
            # Stage 2: Parallel Research
            research_results = await self._run_parallel_research(job, plan)
            job.research_findings = research_results
            
            # Stage 3: Draft
            job.update_status(JobStatus.DRAFTING)
            self._check_cost_limit(job)
            writer = WriterAgent()
            write_output = await writer.execute(job)
            job.draft_content = write_output["draft"]
            
            # Stage 4: Debate (Module 3)
            job.update_status(JobStatus.IN_DEBATE)
            job = await self._run_debate_stage(job)
            
            # Stage 5: HITL Gate (Module 4)
            job.update_status(JobStatus.AWAITING_APPROVAL)
            # Pauses here until human approves — implemented in Module 4
            
            return job
        
        except CostLimitExceededError as e:
            job.update_status(JobStatus.FAILED)
            job.agent_trace.append(AgentTrace(
                agent="orchestrator", action="cost_limit_exceeded",
                started_at=datetime.now(), duration_s=0, error=str(e)
            ))
            raise
    
    def _check_cost_limit(self, job: ContentJob) -> None:
        if job.total_cost_usd > MAX_COST_PER_JOB_USD:
            raise CostLimitExceededError(
                f"Job {job.job_id} exceeded cost limit: "
                f"${job.total_cost_usd:.4f} > ${MAX_COST_PER_JOB_USD}"
            )
    
    async def _run_parallel_research(self, job: ContentJob, plan: dict) -> list[dict]:
        """Runs one ResearcherAgent per research angle, all simultaneously."""
        # Implemented fully in Lesson 2.4
        pass

class CostLimitExceededError(Exception):
    pass
```

---

## Lesson 2.3 — Building the Specialist Agents (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

**ResearcherAgent — gathers information for one angle**

```python
# agents/researcher.py
import json
from agents.base import BaseAgent
from models.job import ContentJob

class ResearcherAgent(BaseAgent):
    def __init__(self, angle: str, angle_index: int):
        super().__init__(f"researcher_{angle_index}")
        self.angle = angle
    
    async def run(self, job: ContentJob) -> dict:
        """
        Researches one specific angle. Uses web search tool for current information.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1200,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3
            }],
            messages=[{
                "role": "user",
                "content": f"""
Research this specific angle for a content piece on "{job.brief.topic}":

<research_angle>
{self.angle}
</research_angle>

Target audience: {job.brief.audience}

Find specific, credible information. Return JSON with:
- "angle": the angle you researched
- "key_facts": list of 3–5 specific, citable facts
- "expert_perspectives": any notable expert views or quotes
- "data_points": specific statistics or numbers found
- "sources": list of URLs you found credible

JSON only.
"""
            }]
        )
        
        # Handle tool use in response
        final_text = self._extract_final_text(response)
        findings = json.loads(final_text)
        
        return {
            "_action": "research",
            "_tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "_preview": f"Found {len(findings.get('key_facts', []))} facts for: {self.angle[:50]}",
            "findings": findings
        }
    
    def _extract_final_text(self, response) -> str:
        """Extracts final text response after any tool calls complete."""
        for block in response.content:
            if block.type == "text":
                return block.text
        return "{}"
```

**WriterAgent — drafts the full content piece**

```python
# agents/writer.py
import json
from agents.base import BaseAgent
from models.job import ContentJob

class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("writer")
    
    async def run(self, job: ContentJob) -> dict:
        research_summary = json.dumps(job.research_findings, indent=2)
        
        # Pull brand voice from agent memory if available (Module 3)
        brand_context = job.brief.brand_context or "No specific brand context provided."
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": f"""
Write a {job.brief.format} on: "{job.brief.topic}"

<audience>{job.brief.audience}</audience>
<tone>{job.brief.tone}</tone>
<target_word_count>{job.brief.word_count_target}</target_word_count>
<brand_context>{brand_context}</brand_context>

<research_findings>
{research_summary}
</research_findings>

Return JSON with:
- "title": compelling title
- "body": full content (use markdown formatting)
- "word_count": actual word count
- "key_claims": list of the 3 most important claims you're making

JSON only.
"""
            }]
        )
        
        draft = json.loads(response.content[0].text)
        return {
            "_action": "draft",
            "_tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "_preview": f"Draft: '{draft.get('title', 'Untitled')}' ({draft.get('word_count', 0)} words)",
            "draft": draft
        }
```

---

## Lesson 2.4 — Running Agents in True Parallel (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

**The parallel research implementation:**

```python
# agents/orchestrator.py (completing _run_parallel_research)
import asyncio

async def _run_parallel_research(self, job: ContentJob, plan: dict) -> list[dict]:
    """
    Creates one ResearcherAgent per angle and runs them all simultaneously.
    Returns merged research findings from all angles.
    """
    research_angles = plan.get("research_angles", [])
    
    # Create researcher agents — one per angle
    researchers = [
        ResearcherAgent(angle=angle, angle_index=i)
        for i, angle in enumerate(research_angles)
    ]
    
    print(f"[Orchestrator] Launching {len(researchers)} researchers in parallel...")
    
    # Run all researchers concurrently
    tasks = [researcher.execute(job) for researcher in researchers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Collect successful results, log failures
    findings = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # One researcher failing shouldn't kill the whole job
            logger.warning(
                f"Researcher {i} failed, continuing with partial results",
                error=str(result), job_id=job.job_id
            )
        else:
            findings.append(result.get("findings", {}))
    
    if not findings:
        raise RuntimeError("All researchers failed — cannot continue")
    
    return findings
```

**Why `return_exceptions=True` matters in production:**

Without it, if one `asyncio.gather` task raises an exception, the exception propagates immediately and *cancels the other tasks*. Three researchers running — one fails — the other two get cancelled and their work is lost.

With `return_exceptions=True`, failures are returned as exception objects in the results list. You check for them explicitly and handle gracefully. For parallel agents, this is non-negotiable.

**Timing comparison:**

```python
import time

async def benchmark():
    angles = ["market trends", "technical implementation", "case studies"]
    
    # Sequential
    start = time.time()
    results = []
    for i, angle in enumerate(angles):
        researcher = ResearcherAgent(angle=angle, angle_index=i)
        result = await researcher.execute(job)
        results.append(result)
    print(f"Sequential: {time.time() - start:.1f}s")  # ~24 seconds
    
    # Parallel
    start = time.time()
    researchers = [ResearcherAgent(angle=a, angle_index=i) for i, a in enumerate(angles)]
    results = await asyncio.gather(*[r.execute(job) for r in researchers])
    print(f"Parallel:   {time.time() - start:.1f}s")  # ~9 seconds
```

### Module 2 Checkpoint ✅
ContentForge can now plan a content strategy and run parallel researchers simultaneously.

---
---

# MODULE 3: Agent Debate, Self-Correction & Memory

**Module outcome:** Implement agent debate/critique pattern; build self-correcting agents; give agents persistent memory across sessions.

**Total time:** ~2.5 hours

---

## Lesson 3.1 — The Debate Pattern (Concept)
**Type:** Concept | **Duration:** 20 min

### Hook

A single editor reviewing a draft has one perspective. What if instead, you had an Editor and a Critic who *disagree with each other* about the draft's quality, and have to reach a consensus? The debate surfaces problems that a single reviewer would rationalise away.

This is one of the most powerful patterns in multi-agent AI: not one agent reviewing, but two agents with different mandates challenging each other — and the output is better than either could produce alone.

### Core Content

**The three roles in a debate:**

1. **Editor** — Reviews the draft against objective criteria: accuracy, structure, audience fit, word count. Returns a scored assessment with specific issues.

2. **Critic** — Challenges the Editor's assessment from the reader's perspective: is this actually engaging? Would the target audience care about this? Does it have a memorable hook?

3. **Arbiter (the Writer)** — Receives both perspectives, synthesises the feedback, and decides what to revise. The Writer doesn't blindly follow either — it makes a judgment call.

**Why this beats a single reviewer:** The Editor and Critic have *different failure modes*. The Editor might approve technically correct but boring content. The Critic might push for engagement at the cost of accuracy. The tension between them surfaces both types of problems.

---

## Lesson 3.2 — Building the Editor-Critic Debate (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

```python
# agents/editor.py
import json
from agents.base import BaseAgent
from models.job import ContentJob

class EditorAgent(BaseAgent):
    def __init__(self):
        super().__init__("editor")
    
    async def run(self, job: ContentJob) -> dict:
        draft = job.draft_content
        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": f"""
You are a rigorous editor reviewing this content piece.

<draft>
Title: {draft.get('title')}
Body: {draft.get('body', '')[:2000]}...
Word count: {draft.get('word_count')}
</draft>

<requirements>
Target audience: {job.brief.audience}
Format: {job.brief.format}
Tone: {job.brief.tone}
Target word count: {job.brief.word_count_target}
</requirements>

Evaluate on: accuracy signals, structure, audience fit, completeness, word count adherence.

Return JSON with:
- "score": 1–10
- "passes": list of things done well (be specific)
- "issues": list of specific problems with severity: critical/major/minor
- "recommendation": "approve" | "revise"
- "must_fix": list of things that MUST change before approval

JSON only.
"""
            }]
        )
        assessment = json.loads(response.content[0].text)
        return {
            "_action": "edit",
            "_tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "_preview": f"Editor score: {assessment.get('score')}/10 — {assessment.get('recommendation')}",
            "assessment": assessment
        }

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("critic")
    
    async def run(self, job: ContentJob) -> dict:
        """
        The Critic plays devil's advocate to the Editor.
        Its mandate: challenge the Editor's assessment, focus on reader experience.
        """
        draft = job.draft_content
        editor_assessment = job.debate_transcript[-1] if job.debate_transcript else {}
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": f"""
You are a contrarian critic. Your job is to challenge the editor's assessment
and advocate for the reader's perspective.

<draft_title>{draft.get('title')}</draft_title>
<editor_assessment>{json.dumps(editor_assessment, indent=2)}</editor_assessment>

Question everything the editor approved. Ask:
- Would a {job.brief.audience} actually find this compelling?
- Does the opening hook grab attention in the first 10 seconds?
- Are the claims specific enough to be credible?
- Is there anything the editor MISSED?

Return JSON with:
- "challenge_score": 1–10 (your independent quality score)
- "editor_blind_spots": what the editor missed or got wrong
- "reader_concerns": what a real reader would complain about
- "strengths_editor_missed": positives the editor didn't mention
- "final_verdict": "approve" | "revise" | "major_rewrite"

JSON only.
"""
            }]
        )
        critique = json.loads(response.content[0].text)
        return {
            "_action": "critique",
            "_tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "_preview": f"Critic score: {critique.get('challenge_score')}/10 — {critique.get('final_verdict')}",
            "critique": critique
        }
```

**Running the debate in the orchestrator:**

```python
# agents/orchestrator.py
async def _run_debate_stage(self, job: ContentJob) -> ContentJob:
    """Runs the Editor-Critic debate and feeds results to the Writer for revision."""
    editor = EditorAgent()
    critic = CriticAgent()
    
    # Run Editor and Critic in parallel — they're independent
    editor_result, critic_result = await asyncio.gather(
        editor.execute(job),
        critic.execute(job)
    )
    
    # Record debate in job
    job.debate_transcript.append({
        "round": 1,
        "editor": editor_result["assessment"],
        "critic": critic_result["critique"]
    })
    
    # Decide whether revision is needed
    editor_rec = editor_result["assessment"].get("recommendation")
    critic_verdict = critic_result["critique"].get("final_verdict")
    
    needs_revision = editor_rec == "revise" or critic_verdict in ("revise", "major_rewrite")
    
    if needs_revision:
        writer = WriterAgent()
        # Writer receives both assessments and revises
        revision_output = await writer.revise(job, editor_result["assessment"], critic_result["critique"])
        job.final_content = revision_output["revised_content"]
    else:
        job.final_content = job.draft_content
    
    return job
```

---

## Lesson 3.3 — Self-Correcting Agents (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 30 min

### Core Content

**The WriterAgent's revision method:**

```python
# agents/writer.py (addition)
async def revise(self, job: ContentJob, editor_feedback: dict, critic_feedback: dict) -> dict:
    """
    Revises the draft based on editor and critic feedback.
    The writer synthesises both perspectives — it doesn't blindly follow either.
    """
    response = self.client.messages.create(
        model=self.model,
        max_tokens=3000,
        messages=[{
            "role": "user",
            "content": f"""
You wrote this content piece and have received feedback from an editor and a critic.
Revise it thoughtfully — address the legitimate concerns but use your judgment.

<original_draft>
{json.dumps(job.draft_content, indent=2)}
</original_draft>

<editor_feedback>
Score: {editor_feedback.get('score')}/10
Issues: {json.dumps(editor_feedback.get('issues', []))}
Must fix: {json.dumps(editor_feedback.get('must_fix', []))}
</editor_feedback>

<critic_feedback>
Score: {critic_feedback.get('challenge_score')}/10
Reader concerns: {json.dumps(critic_feedback.get('reader_concerns', []))}
Blind spots: {json.dumps(critic_feedback.get('editor_blind_spots', []))}
</critic_feedback>

Return JSON with:
- "title": revised title (or same if still good)
- "body": revised full content
- "word_count": new word count
- "key_claims": updated key claims
- "revision_notes": what you changed and why

JSON only.
"""
        }]
    )
    
    revised = json.loads(response.content[0].text)
    return {
        "_action": "revise",
        "_tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        "revised_content": revised
    }
```

---

## Lesson 3.4 — Agent Memory: Remembering Brand Voice Across Sessions (Concept + Demo)
**Type:** Concept + Demo | **Duration:** 40 min

### Hook

Every time you start a new conversation with Claude, it knows nothing about your company's tone, your preferred writing style, or what topics you've already covered. For a content operations engine running hundreds of jobs, this is a real problem. Agent memory solves it.

### Core Content

**Two types of agent memory:**

1. **In-context memory** — Injected into the current prompt. Fast, always visible to the model. Limited by token window. Good for: current session context, recent history.

2. **External memory** — Stored in a database or file, retrieved on demand. Unlimited capacity. Good for: brand guidelines, long-term patterns, historical preferences.

ContentForge uses both: brand voice is external memory (loaded at job start), recent content is in-context (injected into writer prompt).

```python
# memory/agent_memory.py
import json
import os
from datetime import datetime
from pathlib import Path

class AgentMemory:
    """
    Persistent memory store for ContentForge agents.
    In production, replace the JSON file backend with Redis or a database.
    """
    
    def __init__(self, memory_file: str = "memory/contentforge_memory.json"):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(exist_ok=True)
        self._memory = self._load()
    
    def _load(self) -> dict:
        if self.memory_file.exists():
            return json.loads(self.memory_file.read_text())
        return {
            "brand_voice": {},
            "successful_patterns": [],
            "content_history": [],
            "quality_scores": []
        }
    
    def _save(self) -> None:
        self.memory_file.write_text(json.dumps(self._memory, indent=2, default=str))
    
    def update_brand_voice(self, feedback: dict) -> None:
        """Updates brand voice guidelines based on approved content patterns."""
        if "approved_tone_notes" in feedback:
            self._memory["brand_voice"]["tone_notes"] = feedback["approved_tone_notes"]
        if "approved_style_examples" in feedback:
            examples = self._memory["brand_voice"].get("style_examples", [])
            examples.append(feedback["approved_style_examples"])
            self._memory["brand_voice"]["style_examples"] = examples[-5:]  # Keep last 5
        self._save()
    
    def get_brand_context(self) -> str:
        """Returns formatted brand context for injection into writer prompts."""
        bv = self._memory.get("brand_voice", {})
        if not bv:
            return "No brand context established yet."
        
        context = "Brand Voice Guidelines (learned from approved content):\n"
        if "tone_notes" in bv:
            context += f"- Tone: {bv['tone_notes']}\n"
        if "style_examples" in bv:
            context += f"- Style examples: {json.dumps(bv['style_examples'][:2])}\n"
        return context
    
    def record_job_outcome(self, job) -> None:
        """Records quality score and patterns from completed jobs."""
        if job.quality_score:
            self._memory["quality_scores"].append({
                "job_id": job.job_id,
                "topic": job.brief.topic,
                "score": job.quality_score,
                "timestamp": datetime.now().isoformat()
            })
        
        # Record successful patterns from high-quality jobs
        if job.quality_score and job.quality_score >= 8.0:
            self._memory["successful_patterns"].append({
                "format": job.brief.format,
                "audience": job.brief.audience,
                "structure": [s.get("title") for s in (job.final_content or {}).get("sections", [])]
            })
            # Keep only last 20 patterns
            self._memory["successful_patterns"] = self._memory["successful_patterns"][-20:]
        
        self._save()
    
    def get_7day_quality_trend(self) -> float | None:
        """Returns the average quality score over the last 7 days."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=7)
        recent = [
            s["score"] for s in self._memory["quality_scores"]
            if datetime.fromisoformat(s["timestamp"]) > cutoff
        ]
        return sum(recent) / len(recent) if recent else None
```

**Injecting memory into the Writer:**

```python
# In WriterAgent.run() — update the message to include memory context
from memory.agent_memory import AgentMemory

memory = AgentMemory()
brand_context = memory.get_brand_context()

# Include in writer prompt
content = f"""
<brand_context>
{brand_context}
</brand_context>
...rest of prompt
"""
```

### Module 3 Checkpoint ✅
ContentForge agents now debate quality, revise based on synthesised feedback, and carry brand voice memory across all sessions.

---
---

# MODULE 4: Human-in-the-Loop & Agent State Machines

**Module outcome:** Implement a real HITL approval gate; design agent coordination as an explicit state machine.

**Total time:** ~1.5 hours

---

## Lesson 4.1 — When to Stop and Ask a Human (Concept)
**Type:** Concept | **Duration:** 15 min

### Core Content

**The rule for HITL gates:** A human must be in the loop any time the *consequences of being wrong are asymmetric* — where one type of error is far more costly than another.

For ContentForge:
- If we publish bad content → brand damage, public, hard to undo
- If we delay publishing for approval → slightly slower, no lasting harm

The approval gate lives between "revision complete" and "publish." It's non-negotiable.

**What HITL looks like in a async pipeline:**

```
[Job hits AWAITING_APPROVAL status]
         ↓
[Notification sent to approver (Slack via MCP)]
         ↓
[Job is suspended — paused in queue, not consuming resources]
         ↓
[Approver reviews via a simple API endpoint or dashboard]
         ↓
[Approver calls: POST /jobs/{job_id}/approve or /reject with feedback]
         ↓
[Job resumes from AWAITING_APPROVAL → publishing]
```

---

## Lesson 4.2 — Implementing the HITL Approval Gate (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

```python
# agents/orchestrator.py
import asyncio

async def wait_for_approval(self, job: ContentJob, timeout_seconds: int = 86400) -> bool:
    """
    Suspends the job until a human approves or rejects it.
    Polls every 30 seconds. Times out after timeout_seconds (default: 24 hours).
    """
    from queue.approval_store import ApprovalStore
    
    store = ApprovalStore()
    store.set_pending(job.job_id, job.final_content)
    
    # Notify approver via Slack (MCP — Module 6)
    await self._notify_approver(job)
    
    logger.info("Job awaiting approval", job_id=job.job_id)
    
    elapsed = 0
    poll_interval = 30
    
    while elapsed < timeout_seconds:
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
        
        decision = store.get_decision(job.job_id)
        
        if decision is None:
            continue  # Still pending
        
        if decision["status"] == "approved":
            job.approval_status = "approved"
            job.approved_by = decision.get("approver_id", "unknown")
            
            # Update brand memory with any tone notes from approver
            if "feedback" in decision:
                memory = AgentMemory()
                memory.update_brand_voice(decision["feedback"])
            
            return True
        
        elif decision["status"] == "rejected":
            job.approval_status = "rejected"
            # Could trigger another revision cycle here
            return False
    
    # Timeout — escalate
    logger.warning("Approval timeout reached", job_id=job.job_id, timeout_s=timeout_seconds)
    job.approval_status = "timeout"
    return False
```

**The approval store (simple Redis-backed):**

```python
# queue/approval_store.py
import json
import redis
from config import CELERY_BROKER_URL

class ApprovalStore:
    def __init__(self):
        self.r = redis.from_url(CELERY_BROKER_URL)
    
    def set_pending(self, job_id: str, content: dict) -> None:
        self.r.setex(
            f"approval:{job_id}",
            86400,  # 24 hour TTL
            json.dumps({"status": "pending", "content": content})
        )
    
    def approve(self, job_id: str, approver_id: str, feedback: dict = None) -> None:
        self.r.setex(
            f"approval:{job_id}", 86400,
            json.dumps({"status": "approved", "approver_id": approver_id, "feedback": feedback or {}})
        )
    
    def reject(self, job_id: str, reason: str) -> None:
        self.r.setex(
            f"approval:{job_id}", 86400,
            json.dumps({"status": "rejected", "reason": reason})
        )
    
    def get_decision(self, job_id: str) -> dict | None:
        data = self.r.get(f"approval:{job_id}")
        if not data:
            return None
        decision = json.loads(data)
        return decision if decision["status"] != "pending" else None
```

### Module 4 Checkpoint ✅
ContentForge now has all 6 agent patterns implemented: orchestrator-worker, parallel, debate, self-correcting, HITL, and memory.

---
---

# MODULE 5: Deep MCP — Production Servers

**Module outcome:** Build ContentForge's own production MCP server with authentication; understand deployment and versioning.

**Total time:** ~2.5 hours

---

## Lesson 5.1 — What "Production MCP" Means (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

The MCP server you built in Course 2 used stdio — fine for a single machine, useless when a team of 10 developers' tools all need to connect to it. A production MCP server needs:

1. **Network transport** — HTTP/SSE so remote clients can connect
2. **Authentication** — Not everyone should be able to call your tools
3. **Versioning** — Tools change; clients need to know what version they're talking to
4. **Error handling** — Descriptive errors that help clients debug
5. **Deployment** — Runs persistently, restarts on crash, accessible via stable URL

---

## Lesson 5.2 — Building ContentForge's Production MCP Server (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 50 min

### Core Content

```python
# mcp/server/contentforge_server.py
import json
import hmac
import hashlib
from datetime import datetime
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from mcp import types
import uvicorn

SERVER_VERSION = "1.2.0"

server = Server("contentforge-mcp")

# ─── Authentication Middleware ────────────────────────────────────────────
class BearerAuthMiddleware(BaseHTTPMiddleware):
    """Validates Bearer tokens on every MCP request."""
    
    VALID_TOKENS = set(os.getenv("MCP_AUTH_TOKENS", "").split(","))
    
    async def dispatch(self, request, call_next):
        # Skip auth for health check
        if request.url.path == "/health":
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Missing Bearer token"}, status_code=401)
        
        token = auth_header[7:]
        if token not in self.VALID_TOKENS:
            return JSONResponse({"error": "Invalid token"}, status_code=403)
        
        return await call_next(request)

# ─── Tool Definitions ─────────────────────────────────────────────────────
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="submit_content_job",
            description=f"""
                Submit a new content generation job to ContentForge (server v{SERVER_VERSION}).
                ContentForge will research, draft, edit, and publish the content automatically.
                Returns a job_id you can use to track progress.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "The content topic"},
                    "audience": {"type": "string", "description": "Target audience description"},
                    "format": {
                        "type": "string",
                        "enum": ["blog_post", "newsletter", "technical_doc", "social_post"]
                    },
                    "platforms": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["github", "notion", "slack"]}
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "normal", "high"],
                        "default": "normal"
                    }
                },
                "required": ["topic", "audience", "format", "platforms"]
            }
        ),
        types.Tool(
            name="get_job_status",
            description="Get the current status and metrics of a ContentForge job.",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "The job ID returned by submit_content_job"}
                },
                "required": ["job_id"]
            }
        ),
        types.Tool(
            name="approve_job",
            description="Approve a job that is awaiting human review before publishing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string"},
                    "approver_id": {"type": "string", "description": "ID of the person approving"},
                    "tone_feedback": {"type": "string", "description": "Optional tone/style notes to remember"}
                },
                "required": ["job_id", "approver_id"]
            }
        ),
        types.Tool(
            name="get_quality_metrics",
            description="Get ContentForge quality metrics: average score, cost trends, job volume.",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    from queue.tasks import submit_job_task
    from queue.approval_store import ApprovalStore
    from memory.agent_memory import AgentMemory
    
    if name == "submit_content_job":
        from models.job import ContentJob, ContentBrief
        
        brief = ContentBrief(**arguments)
        job = ContentJob(brief=brief)
        
        # Submit to Celery queue — non-blocking
        submit_job_task.delay(job.model_dump())
        
        return [types.TextContent(type="text", text=json.dumps({
            "job_id": job.job_id,
            "status": "queued",
            "message": f"Job {job.job_id} submitted. Use get_job_status to track progress.",
            "server_version": SERVER_VERSION
        }))]
    
    elif name == "get_job_status":
        # Load job from persistent store
        # In production: load from database
        return [types.TextContent(type="text", text=json.dumps({
            "job_id": arguments["job_id"],
            "status": "researching",
            "message": "Job store lookup — implement with your database"
        }))]
    
    elif name == "approve_job":
        store = ApprovalStore()
        feedback = {}
        if "tone_feedback" in arguments:
            feedback["approved_tone_notes"] = arguments["tone_feedback"]
        store.approve(arguments["job_id"], arguments["approver_id"], feedback)
        return [types.TextContent(type="text", text=json.dumps({
            "approved": True, "job_id": arguments["job_id"]
        }))]
    
    elif name == "get_quality_metrics":
        memory = AgentMemory()
        return [types.TextContent(type="text", text=json.dumps({
            "7day_avg_quality": memory.get_7day_quality_trend(),
            "server_version": SERVER_VERSION
        }))]

# ─── HTTP Server Setup ────────────────────────────────────────────────────
sse_transport = SseServerTransport("/mcp/messages")

async def handle_sse(request):
    async with sse_transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

app = Starlette(
    routes=[
        Route("/health", lambda r: JSONResponse({"status": "ok", "version": SERVER_VERSION})),
        Mount("/mcp", app=sse_transport.handle_post_message),
        Route("/mcp/sse", endpoint=handle_sse),
    ],
    middleware=[Middleware(BearerAuthMiddleware)]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## Lesson 5.3 — Versioning, Deployment & Testing the Inspector (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 40 min

### Core Content

**Server versioning — why it matters:**

When you update a tool's schema (add a parameter, rename one, change an enum), clients that are already connected may break. Version your server and communicate breaking changes.

```python
# Convention: embed version in tool descriptions
# Use semantic versioning: MAJOR.MINOR.PATCH
# - MAJOR: breaking changes to tool schemas
# - MINOR: new tools or backward-compatible changes
# - PATCH: bug fixes

SERVER_VERSION = "1.2.0"
API_COMPATIBILITY = ">=1.0.0"  # What clients must support
```

**Testing with MCP Inspector:**

```bash
# Install and run the inspector against your running server
npx @modelcontextprotocol/inspector http://localhost:8080/mcp/sse \
  --header "Authorization: Bearer your-test-token"
```

**Deploying with Docker:**

```dockerfile
# mcp/server/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "mcp.server.contentforge_server:app", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
docker build -t contentforge-mcp .
docker run -p 8080:8080 \
  -e MCP_AUTH_TOKENS="token1,token2" \
  -e ANTHROPIC_API_KEY="sk-ant-..." \
  contentforge-mcp
```

### Module 5 Checkpoint ✅
ContentForge has a production MCP server running over HTTP with authentication, semantic versioning, Docker deployment, and Inspector testing.

---
---

# MODULE 6: Deep MCP — Third-Party Integrations & Multi-Server Routing

**Module outcome:** Connect to GitHub, Notion, and Slack MCP servers; build an MCP router that dispatches to the right server.

**Total time:** ~2 hours

---

## Lesson 6.1 — The Third-Party MCP Ecosystem (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**Where to find official MCP servers:**

- GitHub's official MCP: `github.com/github/github-mcp-server`
- Notion's official MCP: `github.com/makenotion/notion-mcp-server`
- Slack's MCP (community): `github.com/modelcontextprotocol/servers`
- Anthropic's curated list: `modelcontextprotocol.io/servers`

**Running a third-party server locally:**

```bash
# GitHub MCP Server (requires Node.js)
npx @modelcontextprotocol/server-github
# Runs on stdio — connect via client

# Notion MCP Server
npx @notionhq/notion-mcp-server
# Requires NOTION_API_KEY env variable
```

---

## Lesson 6.2 — Building the Multi-Server MCP Client (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 50 min

### Core Content

```python
# mcp/clients/multi_server_client.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from typing import Any

class MultiServerMCPClient:
    """
    Routes tool calls to the appropriate MCP server.
    Manages multiple simultaneous server connections.
    """
    
    TOOL_TO_SERVER = {
        # GitHub tools
        "create_pull_request": "github",
        "push_file": "github",
        "create_issue": "github",
        # Notion tools
        "create_page": "notion",
        "append_block": "notion",
        "search_pages": "notion",
        # Slack tools
        "post_message": "slack",
        "create_channel": "slack",
        # ContentForge own server
        "get_quality_metrics": "contentforge",
        "approve_job": "contentforge",
    }
    
    def __init__(self):
        self.sessions: dict[str, ClientSession] = {}
        self._contexts = {}
    
    async def connect_all(self) -> None:
        """Establish connections to all configured MCP servers."""
        from config import GITHUB_MCP_URL, NOTION_MCP_URL, SLACK_MCP_URL, MCP_AUTH_SECRET
        
        # ContentForge own server (HTTP/SSE)
        if MCP_AUTH_SECRET:
            await self._connect_sse("contentforge", f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/mcp/sse",
                                    headers={"Authorization": f"Bearer {MCP_AUTH_SECRET}"})
        
        # GitHub (stdio)
        await self._connect_stdio("github", 
                                  command="npx",
                                  args=["@modelcontextprotocol/server-github"],
                                  env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")})
        
        # Notion (stdio)
        await self._connect_stdio("notion",
                                  command="npx",
                                  args=["@notionhq/notion-mcp-server"],
                                  env={"NOTION_API_KEY": os.getenv("NOTION_API_KEY")})
    
    async def _connect_stdio(self, server_name: str, command: str, args: list, env: dict = None) -> None:
        params = StdioServerParameters(command=command, args=args, env=env)
        ctx = stdio_client(params)
        read, write = await ctx.__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        self.sessions[server_name] = session
        self._contexts[server_name] = ctx
        print(f"Connected to MCP server: {server_name}")
    
    async def _connect_sse(self, server_name: str, url: str, headers: dict = None) -> None:
        ctx = sse_client(url, headers=headers or {})
        read, write = await ctx.__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        self.sessions[server_name] = session
        self._contexts[server_name] = ctx
    
    async def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Routes a tool call to the correct server."""
        server_name = self.TOOL_TO_SERVER.get(tool_name)
        if not server_name:
            raise ValueError(f"No server registered for tool: {tool_name}")
        
        if server_name not in self.sessions:
            raise RuntimeError(f"Server '{server_name}' not connected")
        
        result = await self.sessions[server_name].call_tool(tool_name, arguments)
        return result.content[0].text if result.content else None
    
    async def get_all_tools(self) -> dict[str, list]:
        """Returns tools available across all connected servers."""
        all_tools = {}
        for server_name, session in self.sessions.items():
            result = await session.list_tools()
            all_tools[server_name] = [t.name for t in result.tools]
        return all_tools
    
    async def disconnect_all(self) -> None:
        for name, session in self.sessions.items():
            await session.__aexit__(None, None, None)
            await self._contexts[name].__aexit__(None, None, None)
```

**The PublisherAgent using the multi-server client:**

```python
# agents/publisher.py
import json
from agents.base import BaseAgent
from models.job import ContentJob
from mcp.clients.multi_server_client import MultiServerMCPClient

class PublisherAgent(BaseAgent):
    def __init__(self, mcp_client: MultiServerMCPClient):
        super().__init__("publisher")
        self.mcp = mcp_client
    
    async def run(self, job: ContentJob) -> dict:
        published = []
        content = job.final_content
        
        for platform in job.brief.platforms:
            try:
                if platform == "github":
                    result = await self.mcp.call_tool("push_file", {
                        "path": f"content/{job.job_id}.md",
                        "content": f"# {content['title']}\n\n{content['body']}",
                        "message": f"Add: {content['title']}",
                        "branch": "main"
                    })
                    published.append({"platform": "github", "result": result})
                
                elif platform == "notion":
                    result = await self.mcp.call_tool("create_page", {
                        "parent_id": os.getenv("NOTION_DATABASE_ID"),
                        "title": content["title"],
                        "content": content["body"]
                    })
                    published.append({"platform": "notion", "result": result})
                
                elif platform == "slack":
                    result = await self.mcp.call_tool("post_message", {
                        "channel": os.getenv("SLACK_CONTENT_CHANNEL", "#content"),
                        "text": f"📝 *{content['title']}* has been published!\n{content['body'][:200]}..."
                    })
                    published.append({"platform": "slack", "result": result})
            
            except Exception as e:
                logger.error(f"Failed to publish to {platform}", error=str(e), job_id=job.job_id)
                published.append({"platform": platform, "error": str(e)})
        
        return {
            "_action": "publish",
            "_tokens_used": 0,
            "_preview": f"Published to {len([p for p in published if 'error' not in p])}/{len(job.brief.platforms)} platforms",
            "published_locations": published
        }
```

### Module 6 Checkpoint ✅
ContentForge connects to GitHub, Notion, and Slack via MCP — routing the right tool call to the right server automatically.

---
---

# MODULE 7: Async Pipelines & Task Queues at Scale

**Module outcome:** Run ContentForge via Celery task queues; handle 1,000+ jobs/day without rate limit crashes.

**Total time:** ~2 hours

---

## Lesson 7.1 — Why Synchronous AI Pipelines Break at Scale (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**What breaks first at 1,000 jobs/day:**

At 1 job every 86 seconds, you hit three walls simultaneously:

1. **Rate limits** — Anthropic enforces requests-per-minute and tokens-per-minute limits. 10 jobs running simultaneously means 10x your per-job token rate hitting at once.

2. **Timeouts** — A ContentForge job takes 60–90 seconds. HTTP requests time out. Users get errors. Jobs are silently lost.

3. **Resource exhaustion** — Synchronous Python blocks a thread per job. At 10 concurrent jobs, you've consumed 10 threads waiting on API responses. This doesn't scale.

**The fix: async task queues**

```
User/Trigger → [Job Submitted to Queue] → [Worker Pool Picks Up Jobs] → [Results Stored]
                   (non-blocking)           (N workers, each handles 1 job)
```

Each worker is its own process. Workers pull jobs from the queue independently. Rate limiting is enforced at the worker level. The submitter never blocks.

---

## Lesson 7.2 — Celery Task Queues for ContentForge (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 45 min

### Core Content

```python
# queue/tasks.py
from celery import Celery
from celery.utils.log import get_task_logger
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, JOB_TIMEOUT_SECONDS, MAX_CONCURRENT_JOBS

app = Celery("contentforge", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_time_limit=JOB_TIMEOUT_SECONDS,          # Hard timeout — kills zombie jobs
    task_soft_time_limit=JOB_TIMEOUT_SECONDS - 30, # Soft timeout — triggers graceful shutdown
    worker_concurrency=MAX_CONCURRENT_JOBS,
    worker_prefetch_multiplier=1,  # Don't grab jobs you can't start — fair distribution
    task_acks_late=True,  # Only acknowledge a job AFTER it's complete (prevents lost jobs on crash)
)

task_logger = get_task_logger(__name__)

@app.task(
    bind=True,
    max_retries=2,
    default_retry_delay=30,
    name="contentforge.submit_job"
)
def submit_job_task(self, job_dict: dict) -> dict:
    """
    The main Celery task. Deserialises the job and runs the full ContentForge pipeline.
    Runs in a worker process — completely isolated.
    """
    import asyncio
    from models.job import ContentJob
    from agents.orchestrator import OrchestratorAgent
    
    try:
        job = ContentJob(**job_dict)
        task_logger.info(f"Worker picked up job {job.job_id}")
        
        orchestrator = OrchestratorAgent()
        completed_job = asyncio.run(orchestrator.run_full_pipeline(job))
        
        # Store result (use your database here)
        result = completed_job.model_dump()
        task_logger.info(f"Job {job.job_id} completed — score: {completed_job.quality_score}")
        return result
    
    except SoftTimeLimitExceeded:
        task_logger.warning(f"Job {self.request.id} approaching timeout — shutting down gracefully")
        raise
    
    except Exception as exc:
        task_logger.error(f"Job failed: {exc}", exc_info=True)
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=30 * (self.request.retries + 1))

# Priority queues — urgent jobs jump the line
app.conf.task_routes = {
    "contentforge.submit_job": {"queue": "normal"},
    "contentforge.submit_urgent_job": {"queue": "priority"},
}
```

**Running workers:**

```bash
# Start worker pool (4 concurrent workers, normal queue)
celery -A queue.tasks worker --concurrency=4 -Q normal --loglevel=info

# Start priority worker (separate process, picks up urgent jobs first)
celery -A queue.tasks worker --concurrency=2 -Q priority,normal --loglevel=info

# Monitor all workers in real time
celery -A queue.tasks flower  # Opens web dashboard at localhost:5555
```

---

## Lesson 7.3 — Rate Limit Handling at Scale (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 45 min

### Core Content

```python
# observability/rate_limiter.py
import asyncio
import time
from collections import deque
from config import MAX_REQUESTS_PER_MINUTE, MAX_TOKENS_PER_MINUTE

class TokenBucketRateLimiter:
    """
    Implements a sliding window rate limiter for Anthropic API calls.
    Shared across all agents in the same worker process.
    """
    
    def __init__(self, max_requests_per_minute: int, max_tokens_per_minute: int):
        self.max_rpm = max_requests_per_minute
        self.max_tpm = max_tokens_per_minute
        self.request_times: deque = deque()
        self.token_usage: deque = deque()  # (timestamp, tokens) pairs
        self._lock = asyncio.Lock()
    
    async def acquire(self, estimated_tokens: int = 1000) -> None:
        """
        Blocks until the rate limit allows this request.
        Call this before every API request.
        """
        async with self._lock:
            await self._wait_for_request_capacity()
            await self._wait_for_token_capacity(estimated_tokens)
            
            now = time.time()
            self.request_times.append(now)
            self.token_usage.append((now, estimated_tokens))
    
    async def _wait_for_request_capacity(self) -> None:
        while True:
            now = time.time()
            # Remove requests older than 60 seconds
            while self.request_times and self.request_times[0] < now - 60:
                self.request_times.popleft()
            
            if len(self.request_times) < self.max_rpm:
                return
            
            # Wait until the oldest request is 60s old
            wait_time = 60 - (now - self.request_times[0]) + 0.1
            await asyncio.sleep(wait_time)
    
    async def _wait_for_token_capacity(self, tokens: int) -> None:
        while True:
            now = time.time()
            while self.token_usage and self.token_usage[0][0] < now - 60:
                self.token_usage.popleft()
            
            current_tpm = sum(t for _, t in self.token_usage)
            if current_tpm + tokens <= self.max_tpm:
                return
            
            await asyncio.sleep(1)

# Global rate limiter instance (shared within a worker process)
rate_limiter = TokenBucketRateLimiter(MAX_REQUESTS_PER_MINUTE, MAX_TOKENS_PER_MINUTE)
```

**Integrating rate limiting into BaseAgent:**

```python
# agents/base.py — update the execute() method
async def execute(self, job: ContentJob) -> dict:
    from observability.rate_limiter import rate_limiter
    
    # Acquire rate limit slot before calling the API
    await rate_limiter.acquire(estimated_tokens=2000)
    
    # ... rest of execute() method unchanged
```

### Module 7 Checkpoint ✅
ContentForge processes jobs via Celery workers with priority queues, graceful timeouts, and API rate limiting.

---
---

# MODULE 8: Observability, Cost Control & Rate Limiting

**Module outcome:** Instrument ContentForge with structured logging, real-time cost tracking, and a live monitoring dashboard.

**Total time:** ~2.5 hours

---

## Lesson 8.1 — You Can't Manage What You Can't Measure (Concept)
**Type:** Concept | **Duration:** 15 min

### Core Content

**The five metrics every production AI system must track:**

| Metric | Why it matters | Alert threshold (example) |
|---|---|---|
| Cost per job | Prevents surprise bills; catches runaway loops | > $2.00 per job |
| Tokens per agent | Identifies which agent is most expensive | > 5,000 tokens per agent call |
| Latency per step | Identifies bottlenecks; catches hanging agents | > 60s per stage |
| Quality score trend | Detects prompt drift or degraded outputs | 7-day avg drops > 0.8 |
| Job success rate | Core reliability metric | < 95% over 24 hours |

Without these, you're flying blind.

---

## Lesson 8.2 — Structured Logging for AI Systems (Demo)
**Type:** Demo | **Duration:** 25 min

### Core Content

```python
# observability/logger.py
import structlog
import logging
import sys

def setup_logging(log_level: str = "INFO") -> None:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()  # Machine-readable JSON logs
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=getattr(logging, log_level))

def get_logger(name: str):
    return structlog.get_logger(name)
```

**What structured log lines look like:**

```json
{"event": "Agent 'writer' completed", "job_id": "job_8f3a2c", 
 "duration_s": 12.4, "tokens": 2847, "logger": "agents.writer", 
 "level": "info", "timestamp": "2026-06-13T10:30:45Z"}

{"event": "Agent 'researcher_2' failed", "job_id": "job_8f3a2c",
 "error": "Rate limit exceeded", "logger": "agents.researcher", 
 "level": "error", "timestamp": "2026-06-13T10:30:47Z"}
```

These can be shipped to Datadog, Grafana Loki, CloudWatch — any log aggregation system.

---

## Lesson 8.3 — Cost & Token Tracking (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

```python
# observability/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Prometheus metrics — exportable to Grafana
TOKENS_USED = Counter(
    "contentforge_tokens_total",
    "Total tokens consumed",
    ["agent", "model"]
)
COST_USD = Counter(
    "contentforge_cost_usd_total",
    "Total API cost in USD",
    ["agent"]
)
JOB_LATENCY = Histogram(
    "contentforge_job_duration_seconds",
    "End-to-end job duration",
    buckets=[10, 30, 60, 90, 120, 180, 300]
)
QUALITY_SCORE = Gauge(
    "contentforge_quality_score",
    "Latest job quality score"
)
ACTIVE_JOBS = Gauge(
    "contentforge_active_jobs",
    "Number of currently running jobs"
)
JOB_OUTCOMES = Counter(
    "contentforge_job_outcomes_total",
    "Job success/failure counts",
    ["status"]  # published, failed, rejected
)

MODEL_COSTS = {
    "claude-opus-4-6": 0.000015,        # per token (approximate)
    "claude-sonnet-4-6": 0.000003,
    "claude-haiku-4-5-20251001": 0.00000025,
}

def record_agent_call(agent_name: str, duration: float, tokens: int, cost: float, success: bool) -> None:
    model = "claude-sonnet-4-6"  # Default; pass model if available
    TOKENS_USED.labels(agent=agent_name, model=model).inc(tokens)
    COST_USD.labels(agent=agent_name).inc(cost)

def record_job_completion(job) -> None:
    JOB_LATENCY.observe((datetime.now() - job.created_at).total_seconds())
    if job.quality_score:
        QUALITY_SCORE.set(job.quality_score)
    JOB_OUTCOMES.labels(status=job.status.value).inc()

def start_metrics_server(port: int = 9090) -> None:
    """Expose metrics at /metrics for Prometheus to scrape."""
    start_http_server(port)
    print(f"Metrics server running on port {port}")
```

---

## Lesson 8.4 — Building the Real-Time Observability Dashboard (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 45 min

### Core Content

A lightweight live dashboard using FastAPI + Server-Sent Events:

```python
# observability/dashboard.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import asyncio
import json
from memory.agent_memory import AgentMemory

dashboard_app = FastAPI()

@dashboard_app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>ContentForge Live Dashboard</title>
    <style>
        body { font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .metric { background: #161b22; border: 1px solid #30363d; 
                  border-radius: 6px; padding: 16px; margin: 8px; display: inline-block; min-width: 200px; }
        .metric h3 { color: #58a6ff; margin: 0 0 8px 0; font-size: 12px; text-transform: uppercase; }
        .metric .value { font-size: 28px; font-weight: bold; }
        .good { color: #3fb950; } .warn { color: #d29922; } .bad { color: #f85149; }
        #log { background: #161b22; border: 1px solid #30363d; padding: 16px;
               height: 300px; overflow-y: auto; font-size: 12px; margin-top: 16px; }
    </style>
</head>
<body>
    <h1>🏭 ContentForge Live Dashboard</h1>
    <div id="metrics"></div>
    <div id="log"><em>Connecting to live feed...</em></div>
    
    <script>
        const evtSource = new EventSource("/events");
        evtSource.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            // Update metrics
            const q = data.quality_avg;
            const qClass = q >= 7.5 ? 'good' : q >= 6.0 ? 'warn' : 'bad';
            
            document.getElementById("metrics").innerHTML = `
                <div class="metric">
                    <h3>Jobs Today</h3>
                    <div class="value">${data.jobs_today}</div>
                </div>
                <div class="metric">
                    <h3>Avg Quality Score</h3>
                    <div class="value ${qClass}">${q ? q.toFixed(1) : 'N/A'}</div>
                </div>
                <div class="metric">
                    <h3>Daily Cost</h3>
                    <div class="value ${data.daily_cost > 40 ? 'warn' : 'good'}">
                        $${data.daily_cost.toFixed(2)}
                    </div>
                </div>
                <div class="metric">
                    <h3>Active Jobs</h3>
                    <div class="value">${data.active_jobs}</div>
                </div>
                <div class="metric">
                    <h3>Avg Latency</h3>
                    <div class="value">${data.avg_latency_s.toFixed(0)}s</div>
                </div>
            `;
            
            // Append to log
            const log = document.getElementById("log");
            log.innerHTML += `<div>[${data.timestamp}] ${data.latest_event}</div>`;
            log.scrollTop = log.scrollHeight;
        };
    </script>
</body>
</html>
""")

@dashboard_app.get("/events")
async def events():
    async def generate():
        memory = AgentMemory()
        while True:
            payload = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "quality_avg": memory.get_7day_quality_trend(),
                "jobs_today": 0,       # Pull from your job store
                "daily_cost": 0.0,     # Pull from metrics
                "active_jobs": 0,      # Pull from Celery
                "avg_latency_s": 0.0,  # Pull from metrics
                "latest_event": "Monitoring active"
            }
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(5)  # Update every 5 seconds
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Module 8 Checkpoint ✅
ContentForge has structured JSON logging, Prometheus metrics, and a real-time SSE dashboard.

---
---

# MODULE 9: Resilience & Quality Monitoring in Production

**Module outcome:** Build retry logic with exponential backoff; implement circuit breakers; detect quality drift in production.

**Total time:** ~1.5 hours

---

## Lesson 9.1 — Designing for Failure (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**The three resilience patterns every production AI system needs:**

1. **Retry with exponential backoff** — Transient failures (rate limits, network timeouts) often resolve themselves in seconds. Retry, but wait longer between each attempt to avoid hammering a struggling API.

2. **Circuit breaker** — If an external service (Notion API, GitHub) is consistently failing, stop sending requests and let it recover. Don't waste tokens and time on requests that will fail.

3. **Quality drift detection** — Your prompts may degrade over time without obvious errors. The API returns 200 OK, the content looks plausible, but the average quality score quietly drops 1.5 points over 3 weeks. You need automated detection.

---

## Lesson 9.2 — Retry Logic & Circuit Breakers (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

```python
# observability/resilience.py
import asyncio
import time
from functools import wraps
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import anthropic
import logging

logger = logging.getLogger(__name__)

# ─── Retry Decorator ──────────────────────────────────────────────────────
def with_retry(max_attempts: int = 3, min_wait: float = 1.0, max_wait: float = 60.0):
    """
    Decorator that adds exponential backoff retry to any async function.
    Retries on rate limits and overload errors. Fails immediately on other errors.
    """
    def decorator(func):
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
            retry=retry_if_exception_type((
                anthropic.RateLimitError,
                anthropic.APIStatusError,
                anthropic.APITimeoutError,
                asyncio.TimeoutError,
            )),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True
        )
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# ─── Circuit Breaker ──────────────────────────────────────────────────────
class CircuitBreaker:
    """
    Tracks failure rate for an external service.
    Opens (stops requests) after failure_threshold failures in window_seconds.
    Resets after recovery_timeout_seconds.
    """
    
    def __init__(self, name: str, failure_threshold: int = 5,
                 window_seconds: int = 60, recovery_timeout: int = 120):
        self.name = name
        self.failure_threshold = failure_threshold
        self.window_seconds = window_seconds
        self.recovery_timeout = recovery_timeout
        
        self.failures: list[float] = []
        self.state = "closed"  # closed = normal, open = blocking, half-open = testing
        self.opened_at: float | None = None
    
    def record_success(self) -> None:
        if self.state == "half-open":
            self.state = "closed"
            self.failures = []
            logger.info(f"Circuit breaker '{self.name}': closed (recovered)")
    
    def record_failure(self) -> None:
        now = time.time()
        self.failures = [t for t in self.failures if t > now - self.window_seconds]
        self.failures.append(now)
        
        if len(self.failures) >= self.failure_threshold:
            self.state = "open"
            self.opened_at = now
            logger.warning(f"Circuit breaker '{self.name}': OPEN — {len(self.failures)} failures in {self.window_seconds}s")
    
    def can_execute(self) -> bool:
        if self.state == "closed":
            return True
        
        if self.state == "open":
            if self.opened_at and time.time() - self.opened_at > self.recovery_timeout:
                self.state = "half-open"
                logger.info(f"Circuit breaker '{self.name}': half-open — testing recovery")
                return True
            return False
        
        return True  # half-open: allow one test request

# Usage in PublisherAgent
github_circuit = CircuitBreaker("github-mcp", failure_threshold=3, recovery_timeout=60)

async def publish_to_github_safe(content: dict) -> dict:
    if not github_circuit.can_execute():
        raise RuntimeError("GitHub MCP circuit breaker is OPEN — skipping GitHub publish")
    try:
        result = await mcp_client.call_tool("push_file", {...})
        github_circuit.record_success()
        return result
    except Exception as e:
        github_circuit.record_failure()
        raise
```

---

## Lesson 9.3 — Production Quality Drift Detection (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

```python
# observability/quality_monitor.py
from memory.agent_memory import AgentMemory
from config import QUALITY_DRIFT_ALERT, MIN_QUALITY_SCORE

class QualityMonitor:
    """
    Monitors ContentForge's average quality score over time.
    Detects drift and triggers alerts before humans notice degradation.
    """
    
    def __init__(self):
        self.memory = AgentMemory()
    
    def check_drift(self) -> dict:
        """
        Compares recent quality scores against historical baseline.
        Returns a report with drift status and recommended action.
        """
        scores = self.memory._memory.get("quality_scores", [])
        if len(scores) < 10:
            return {"status": "insufficient_data", "message": "Need at least 10 jobs"}
        
        # Calculate 7-day and 30-day averages
        recent_7d = self._average_over_days(scores, 7)
        baseline_30d = self._average_over_days(scores, 30)
        
        if not recent_7d or not baseline_30d:
            return {"status": "insufficient_data"}
        
        drift = baseline_30d - recent_7d  # Positive = scores dropped
        
        status = "healthy"
        if drift > QUALITY_DRIFT_ALERT:
            status = "degraded"
        elif recent_7d < MIN_QUALITY_SCORE:
            status = "below_threshold"
        
        return {
            "status": status,
            "recent_7d_avg": round(recent_7d, 2),
            "baseline_30d_avg": round(baseline_30d, 2),
            "drift": round(drift, 2),
            "recommendation": self._recommend_action(status, drift),
            "jobs_analysed": len(scores)
        }
    
    def _average_over_days(self, scores: list, days: int) -> float | None:
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        relevant = [s["score"] for s in scores
                    if datetime.fromisoformat(s["timestamp"]) > cutoff]
        return sum(relevant) / len(relevant) if relevant else None
    
    def _recommend_action(self, status: str, drift: float) -> str:
        if status == "healthy":
            return "No action required"
        elif status == "below_threshold":
            return "Quality below minimum — review recent prompts and eval results immediately"
        elif drift > 1.5:
            return "Significant drift detected — run full eval suite, check for API model changes"
        else:
            return "Moderate drift — review eval scores for specific failure patterns"
```

**Scheduling quality checks:**

```python
# In Celery: run quality check daily
@app.task(name="contentforge.quality_check")
def daily_quality_check():
    monitor = QualityMonitor()
    report = monitor.check_drift()
    
    if report["status"] != "healthy":
        # Alert via Slack MCP
        asyncio.run(notify_team(
            f"⚠️ ContentForge quality alert: {report['status']}\n"
            f"7-day avg: {report.get('recent_7d_avg')} | Baseline: {report.get('baseline_30d_avg')}\n"
            f"Action: {report.get('recommendation')}"
        ))
    
    return report

# Schedule with Celery Beat
app.conf.beat_schedule = {
    "daily-quality-check": {
        "task": "contentforge.quality_check",
        "schedule": crontab(hour=9, minute=0),  # 9am every day
    }
}
```

### Module 9 Checkpoint ✅
ContentForge now retries transient failures, protects itself from cascading failures with circuit breakers, and proactively alerts on quality degradation.

---
---

# MODULE 10: Claude Code as an Orchestrated Agent

**Module outcome:** Spawn and orchestrate Claude Code programmatically within the ContentForge pipeline.

**Total time:** ~1.5 hours

---

## Lesson 10.1 — Claude Code's Programmatic Interface (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

Claude Code is an AI coding assistant you can run from the terminal — but for ContentForge, the more powerful use is running it *programmatically*: ContentForge spawns Claude Code as a subprocess, gives it a task, captures its output, and uses the result.

Why? For technical content (tutorials, documentation, code examples), having Claude Code actually *write and run the code* before the WriterAgent includes it in an article is dramatically better than asking a conversational model to imagine what working code looks like.

**The interface:** Claude Code accepts tasks via `--print` flag for non-interactive use:

```bash
claude --print "Create a Python function that implements binary search with full docstring and type hints. Only output the code, no explanation."
```

**Programmatic invocation from Python:**

```python
import subprocess
import asyncio

async def invoke_claude_code(task: str, working_dir: str = "/tmp") -> str:
    """
    Invokes Claude Code non-interactively and captures output.
    Returns the generated code/output as a string.
    """
    process = await asyncio.create_subprocess_exec(
        "claude", "--print", task,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=working_dir
    )
    stdout, stderr = await asyncio.wait_for(
        process.communicate(),
        timeout=120  # Claude Code tasks can take time
    )
    
    if process.returncode != 0:
        raise RuntimeError(f"Claude Code failed: {stderr.decode()}")
    
    return stdout.decode()
```

---

## Lesson 10.2 — ContentForge's Code Content Agent (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 35 min

### Core Content

For technical blog posts, ContentForge spawns Claude Code to generate verified, working code examples:

```python
# agents/code_content_agent.py
import asyncio
import tempfile
import subprocess
from pathlib import Path
from agents.base import BaseAgent
from models.job import ContentJob

class CodeContentAgent(BaseAgent):
    """
    Uses Claude Code to generate working code examples for technical content.
    Spawned by the WriterAgent when the brief calls for code-heavy content.
    """
    
    def __init__(self):
        super().__init__("code_content")
    
    async def run(self, job: ContentJob) -> dict:
        """
        Generates code examples and validates they run without errors.
        Returns code blocks ready for injection into the article.
        """
        code_examples = []
        
        for key_claim in (job.draft_content or {}).get("key_claims", []):
            if self._needs_code_example(key_claim):
                example = await self._generate_and_verify_code(
                    claim=key_claim,
                    topic=job.brief.topic,
                    audience=job.brief.audience
                )
                if example:
                    code_examples.append(example)
        
        return {
            "_action": "generate_code",
            "_tokens_used": 0,  # Claude Code billing is separate
            "_preview": f"Generated {len(code_examples)} verified code examples",
            "code_examples": code_examples
        }
    
    async def _generate_and_verify_code(self, claim: str, topic: str, audience: str) -> dict | None:
        """Generates a code example and verifies it runs."""
        task = f"""
For a technical article about "{topic}" aimed at {audience}:

Write a complete, working Python code example that demonstrates: {claim}

Requirements:
- Full working code (not pseudocode)
- Proper imports
- Type hints
- Docstring on the main function
- A simple test/usage example at the bottom in if __name__ == "__main__"

Output ONLY the Python code. No explanation. No markdown fences.
"""
        
        try:
            code = await invoke_claude_code(task)
            
            # Verify the code actually runs
            is_valid, error = await self._verify_runs(code)
            
            return {
                "claim": claim,
                "code": code,
                "language": "python",
                "verified_runs": is_valid,
                "syntax_error": error if not is_valid else None
            }
        except Exception as e:
            logger.warning(f"Code generation failed for claim: {claim[:50]}", error=str(e))
            return None
    
    async def _verify_runs(self, code: str) -> tuple[bool, str | None]:
        """Runs the generated code in a subprocess to verify it executes without errors."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            tmp_path = f.name
        
        try:
            result = await asyncio.create_subprocess_exec(
                "python", tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await asyncio.wait_for(result.communicate(), timeout=10)
            
            if result.returncode == 0:
                return True, None
            return False, stderr.decode()[:500]
        except asyncio.TimeoutError:
            return False, "Execution timed out"
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    def _needs_code_example(self, claim: str) -> bool:
        code_keywords = ["implement", "build", "create", "function", "algorithm", "pattern", "api"]
        return any(kw in claim.lower() for kw in code_keywords)
```

### Module 10 Checkpoint ✅
ContentForge spawns Claude Code to generate and verify working code examples before including them in technical content.

---
---

# MODULE 11: Computer Use — Real Browser Automation

**Module outcome:** Build a Computer Use application that verifies published ContentForge posts render correctly in a real browser.

**Total time:** ~2 hours

---

## Lesson 11.1 — How Computer Use Actually Works (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**The architecture:**

Computer Use is not magic — it's the same tool-use pattern you already know, but the tools are: `screenshot()`, `mouse_move(x, y)`, `left_click(x, y)`, `type(text)`, `key(key_name)`.

Claude receives a screenshot, analyses it visually, decides what to click or type, and sends a tool call. Your code executes that action against a real computing environment (a Docker container running a desktop), takes a new screenshot, and sends it back. Repeat until the task is done.

```
[Claude] "I see a login form. I should click the email field."
    ↓
[Tool call: left_click(x=340, y=280)]
    ↓
[Your code: execute click in Docker container]
    ↓
[Take new screenshot → send to Claude]
    ↓
[Claude] "The email field is now focused. I'll type the address."
    ↓
[Tool call: type(text="user@example.com")]
    ↓
... repeats until task complete
```

**The Docker setup:** Anthropic provides a reference Docker image with a full Linux desktop, Xvfb virtual display, Firefox, and VNC. You interact with it via a simple HTTP API.

---

## Lesson 11.2 — Docker Setup & Reference Implementation (Demo)
**Type:** Demo | **Duration:** 30 min

### Core Content

```bash
# Pull Anthropic's computer use reference image
docker pull ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

# Run with VNC enabled for visual inspection
docker run -it \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $HOME/.anthropic:/home/user/.anthropic \
  -p 5900:5900 \   # VNC port (connect with any VNC client to watch in real-time)
  -p 8501:8501 \   # Streamlit demo interface
  ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

# Connect a VNC client to localhost:5900 to watch Claude navigate
```

**Programmatic control (bypassing the demo UI):**

```python
# computer_use/docker_client.py
import httpx
import base64

class ComputerUseDockerClient:
    """HTTP client for the computer use Docker container's control API."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.http = httpx.AsyncClient(timeout=30.0)
    
    async def screenshot(self) -> bytes:
        """Takes a screenshot of the virtual display and returns raw PNG bytes."""
        response = await self.http.get(f"{self.base_url}/screenshot")
        return base64.b64decode(response.json()["image"])
    
    async def click(self, x: int, y: int) -> None:
        await self.http.post(f"{self.base_url}/action", json={"type": "click", "x": x, "y": y})
    
    async def type_text(self, text: str) -> None:
        await self.http.post(f"{self.base_url}/action", json={"type": "type", "text": text})
    
    async def navigate(self, url: str) -> None:
        await self.http.post(f"{self.base_url}/action", json={"type": "navigate", "url": url})
```

---

## Lesson 11.3 — ContentForge's Content Verification Agent (Demo + Practice)
**Type:** Demo + Practice | **Duration:** 50 min

### Core Content

After publishing, ContentForge's VerifierAgent navigates to the published URL, takes a screenshot, and asks Claude: "Does this look correctly formatted? Are there any obvious rendering issues?"

```python
# computer_use/verifier.py
import base64
import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL
from computer_use.docker_client import ComputerUseDockerClient

COMPUTER_USE_TOOLS = [
    {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": 1280,
        "display_height_px": 800,
        "display_number": 1
    }
]

class ContentVerifierAgent:
    """
    Uses Claude Computer Use to visually verify published content in a real browser.
    Checks: page loads, title matches, no 404s, content renders correctly.
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.docker = ComputerUseDockerClient()
    
    async def verify(self, job_id: str, published_locations: list[dict]) -> dict:
        """Verifies all published locations for a job."""
        results = []
        for location in published_locations:
            result = await self._verify_url(
                url=location.get("url"),
                platform=location.get("platform"),
                expected_title=None  # Will check visually
            )
            results.append({"platform": location["platform"], **result})
        return {"job_id": job_id, "verification_results": results}
    
    async def _verify_url(self, url: str, platform: str, expected_title: str = None) -> dict:
        """Navigates to URL and verifies the page renders correctly."""
        
        # Navigate to the URL
        await self.docker.navigate(url)
        await asyncio.sleep(3)  # Wait for page to load
        
        # Take initial screenshot
        screenshot_bytes = await self.docker.screenshot()
        screenshot_b64 = base64.standard_b64encode(screenshot_bytes).decode()
        
        # Ask Claude to analyse the page visually
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": screenshot_b64
                    }
                },
                {
                    "type": "text",
                    "text": f"""
You are verifying that a published article rendered correctly on {platform}.
URL: {url}

Look at the screenshot and check:
1. Did the page load? (No 404, no error messages)
2. Is there readable text content? (Not blank, not garbled)
3. Are there any obvious rendering issues? (Broken images, malformed tables, cut-off text)
4. Does the layout look appropriate for a {platform} article?

Use the computer tool if you need to scroll down to check more content.

Then return JSON: {{"page_loaded": bool, "content_visible": bool, "rendering_issues": [], 
"overall_status": "pass" | "warn" | "fail", "notes": "..."}}
"""
                }
            ]
        }]
        
        # Run the verification loop
        while True:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=1000,
                tools=COMPUTER_USE_TOOLS,
                messages=messages,
                betas=["computer-use-2025-01-24"]
            )
            
            # If Claude wants to interact with the browser
            if response.stop_reason == "tool_use":
                tool_result_content = []
                for block in response.content:
                    if block.type == "tool_use" and block.name == "computer":
                        action = block.input.get("action")
                        
                        # Execute the requested action
                        if action == "screenshot":
                            screenshot_bytes = await self.docker.screenshot()
                            screenshot_b64 = base64.standard_b64encode(screenshot_bytes).decode()
                            tool_result_content.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}}]
                            })
                        elif action == "left_click":
                            await self.docker.click(block.input["coordinate"][0], block.input["coordinate"][1])
                            tool_result_content.append({"type": "tool_result", "tool_use_id": block.id, "content": "Click executed"})
                        elif action == "scroll":
                            # Scroll handled by click-and-drag in the docker client
                            tool_result_content.append({"type": "tool_result", "tool_use_id": block.id, "content": "Scroll executed"})
                
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_result_content})
            
            else:
                # Claude gave a final text response — extract the JSON
                final_text = next(
                    (block.text for block in response.content if block.type == "text"), "{}"
                )
                return json.loads(final_text)
```

---

## Lesson 11.4 — Production Considerations for Computer Use (Concept)
**Type:** Concept | **Duration:** 20 min

### Core Content

**What to know before using Computer Use in production:**

1. **Cost** — Computer Use is token-expensive. Screenshots are large images (each = ~1,500 input tokens). A 10-action verification task = ~15,000 tokens. Budget accordingly.

2. **Latency** — Each action-screenshot cycle is 3–8 seconds. A 5-step verification = ~30 seconds. This is fine for async verification; terrible for real-time user-facing features.

3. **Determinism** — Computer Use is less deterministic than tool use. Page layouts change. A button moves 10px and Claude clicks slightly wrong. Build retries and fallback verification methods (direct API checks, HTML parsing).

4. **When to use vs. alternatives:**

| Situation | Computer Use | Alternative |
|---|---|---|
| Verify a GitHub PR was created | ✓ Visual confirmation | GitHub API check (faster, cheaper) |
| Verify Notion page renders markdown correctly | ✓ Visual only | N/A — no API for visual rendering |
| Fill a web form with no API | ✓ Only option | Build an API integration |
| Verify a public website looks correct | ✓ | Playwright/Selenium (faster, no AI cost) |

Use Computer Use when visual verification is genuinely required and no programmatic alternative exists.

### Module 11 Checkpoint ✅
ContentForge visually verifies all published content renders correctly in a real browser.

---
---

# FINAL PROJECT: ContentForge Deployment

**The challenge:** Deploy ContentForge as a running system for one week and report real production data.

**Phases:**

**Phase 1 — Build (3–4 hrs):** Assemble the complete ContentForge system, connect all MCP servers, confirm all agent patterns are functional, verify the Celery queue processes jobs end-to-end.

**Phase 2 — Run (3–5 hrs):** Submit 25 real content jobs across all 4 formats and 3+ platforms. Let the system run with HITL enabled — approve jobs yourself. Collect real metrics.

**Phase 3 — Report (2–3 hrs):** Produce a production report covering: average quality score and trend, cost per job breakdown by agent, P50/P90/P99 job latency, jobs that hit circuit breakers or retries, quality drift check results, one specific failure you diagnosed and fixed.

**Deliverables:**
1. Running ContentForge codebase (GitHub repo)
2. Production report (markdown document)
3. 5 examples of published content with verification screenshots

---

## Final Project Rubric

| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|---|---|---|---|---|
| **All 6 agent patterns** (30%) | All 6 implemented, clearly distinct, production-grade error handling | 5 of 6 patterns, basic error handling | 3–4 patterns | Fewer than 3 |
| **Production scale** (30%) | Celery queue, rate limiter, circuit breakers, observability dashboard all functional; real data from ≥25 jobs | 3 of 4 components, ≥10 jobs | 2 components, ≥5 jobs | 1 component or fewer than 5 jobs |
| **MCP integration** (20%) | Own server deployed + 2 third-party servers connected, multi-server routing working | Own server + 1 third-party | Own server only | No MCP beyond Course 2 |
| **Production report** (20%) | All 6 required metrics with real data, one diagnosed failure, quality trend analysed | 4 of 6 metrics, partial analysis | 2–3 metrics, no analysis | No report or placeholder data |

---

---

# Appendix: Assessment Plan

| Assessment | After Module | Type | Outcomes | Est. Time |
|---|---|---|---|---|
| Quiz 1: Architecture | Module 2 | 10 MCQ | 1 | 15 min |
| Assignment 1: Agent Pattern Analysis | Module 4 | Code + diagram | 1 | 3 hrs |
| Quiz 2: MCP | Module 6 | 10 MCQ + 2 short answer | 2 | 25 min |
| Assignment 2: Observability Build | Module 9 | Code + dashboard demo | 3, 4, 5 | 3 hrs |
| Quiz 3: Production Scale | Module 9 | 10 MCQ | 3, 4, 5 | 15 min |
| Final Project | Full course | Build + report | 1–7 | 8–12 hrs |

---

## Module Quiz Topics

**Quiz 1 (Architecture + Multi-Agent):**
Why agents need a shared job model; orchestrator vs. specialist responsibilities; `return_exceptions=True` in asyncio.gather; agent debate pattern mechanics; when HITL is non-negotiable; agent memory types (in-context vs. external)

**Quiz 2 (MCP):**
stdio vs. HTTP/SSE transport trade-offs; what semantic versioning means for MCP servers; how BearerAuth middleware intercepts requests; TOOL_TO_SERVER routing pattern; when circuit breakers apply to MCP calls; difference between resources and tools at the server level

**Quiz 3 (Production Scale):**
Token bucket vs. fixed window rate limiting; `task_acks_late=True` in Celery and why it prevents data loss; circuit breaker states (closed, open, half-open); what quality drift detection catches that error rates don't; Prometheus metric types (counter vs. gauge vs. histogram); why SSE is appropriate for the observability dashboard

---

## Series Completion: What Graduates Can Build

A developer who completes all three courses can architect and ship:

- **Multi-agent production systems** that coordinate specialist AI agents with debate, memory, and self-correction
- **End-to-end AI pipelines** that are tested, monitored, cost-controlled, and resilient to failure
- **MCP servers and ecosystems** that other tools and teams can connect to
- **AI-powered development workflows** using Claude Code as an orchestrated agent
- **Production deployments** with observability dashboards, quality drift detection, and automatic alerting

This is the complete picture: from your first `client.messages.create()` call in Course 1 to architecting distributed AI systems in Course 3.

---

## Notes for Course Expansion

- Module 2's parallel research pattern could include a dedicated asyncio patterns primer for learners less confident with coroutines
- Module 3's debate pattern is a natural candidate for a case study lesson showing real Editor/Critic transcripts from actual runs
- Module 5's MCP deployment section can be extended with Terraform/cloud deployment (AWS ECS, Railway, Fly.io) with full infrastructure-as-code
- Module 7's Celery section pairs well with a monitoring lab using Flower dashboard and Redis Commander
- Module 8's observability dashboard can be upgraded to a full Grafana integration with Prometheus scraping
- Module 9's quality drift detection could include anomaly detection using simple statistical process control (control charts) rather than fixed thresholds
- Module 10's Claude Code orchestration can be expanded with custom commands and the parallel worktrees pattern from the reference notes
- Module 11's Computer Use section can be extended with Playwright as a cheaper alternative for cases where visual AI isn't needed
