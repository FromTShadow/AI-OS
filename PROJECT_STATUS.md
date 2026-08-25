# AI-OS Project Status

## Project

AI-OS is a local-first AI operating system running on a MacBook Pro and designed as a modular personal AI platform.

The long-term goal is to combine:

* Local AI models
* Shared memory
* Personal Second Brain
* Research automation
* Software development
* Website development
* Trading systems
* Multi-agent execution
* Business automation
* Long-running autonomous research

The system is designed for maintainability and extensibility rather than quick one-off scripts.

---

## Current Development Version

**AI-OS v0.3.2-dev**

Latest stable Git checkpoint:

`b8deed2 - Make current project state authoritative over memory`

---

## Current Architecture

Current execution flow:

User Request
→ Task
→ Planner
→ Specialist Router
→ Current Project State
→ Qdrant Memory Retrieval
→ Context Builder
→ Prompt Builder
→ Ollama
→ Answer + Metadata

### Core Principle

**Current project state is authoritative.**

Historical Obsidian/Qdrant memory may contain old plans or completed work and must never override the latest State information.

---

## Completed Components

### Infrastructure

* Docker
* Ollama
* Open WebUI
* Qdrant
* PostgreSQL
* n8n
* Obsidian

### Models

* `qwen3:14b`
* `nomic-embed-text`

Embedding size:

`768`

### Brain Architecture

* Task object
* Execution Pipeline
* Planner v1
* Specialist Router
* Prompt Loader
* Versioned Markdown prompts
* Current State provider
* Semantic Qdrant memory
* Chunked Obsidian indexing
* Unique-note retrieval
* Context builder / prototype memory compressor
* Source reporting
* Execution metadata
* Git version control

### Specialist Roles

* Developer
* Research
* Second Brain
* Trading
* CEO

---

## Current State

### Complete

* Planner
* Execution Pipeline
* Memory Search
* Prompt Loader
* Router
* State Provider

### In Progress

* Context Builder

### Needs Improvement

* Memory Compressor

### Planned

* LLM Planner
* Multi-Agent Execution

Current development focus:

**Context authority and state priority**

Next planned focus:

**Intelligent memory retrieval/reranking, memory compression, and pipeline tests**

---

## Important Design Decisions

### Task-Based Architecture

Pipeline components should increasingly accept and return the same Task object.

Target style:

`task = stage.process(task)`

This prevents large parameter lists and makes future orchestration easier.

The Task may eventually be renamed to `ExecutionContext`.

### State vs Memory

State represents current reality.

Memory represents historical and long-term knowledge.

Priority:

1. Current State
2. Execution/Planner information
3. Historical Memory

Memory must never override current State.

### Prompt Architecture

Prompts are stored as versioned Markdown files instead of hardcoded Python strings.

Current prompt types:

* System
* Developer
* Research
* Second Brain
* Trading
* CEO

### Open WebUI

AI-OS should remain independent from Open WebUI.

Open WebUI should be treated as a frontend/interface rather than the core architecture.

Future integrations should prefer:

* API
* OpenAPI
* MCP

rather than tightly coupling AI-OS to legacy Open WebUI Pipeline plugins.

---

## Python Environment

Current environment:

`~/AI-OS/.venv`

Current Python:

`Python 3.13.15`

Status:

**Migration completed and end-to-end validated.**

The previous environment:

`~/AI-OS/projects/knowledge-system/venv`

is retained temporarily as a rollback environment and should only be removed after the migration commit is finalized and one additional clean-start validation passes.

### Planned Migration

Create:

`~/AI-OS/.venv`

Target:

**Python 3.12+**

Migration must use a checklist.

### Migration Checklist

* Create root `.venv`
* Install dependencies
* Test configuration
* Test Ollama
* Test Qdrant
* Test memory search
* Test indexing
* Test Planner
* Test Router
* Test State Provider
* Test Prompt Loader
* Test Execution Pipeline
* Run end-to-end Brain test
* Verify Open WebUI integrations
* Verify PostgreSQL
* Verify n8n
* Commit migration
* Remove old venv only after all tests pass

---

## Near-Term Roadmap

### 1. Modern Python Migration

Move AI-OS to a root Python 3.12+ environment.

Do not remove the current venv until all tests pass.

### 2. Local Model Benchmark

Do not blindly replace `qwen3:14b`.

Benchmark several modern local models against real AI-OS workloads.

Evaluation criteria:

* Planning accuracy
* Coding quality
* Tool use
* Research reasoning
* Memory-grounded answers
* Speed
* RAM usage
* Long-running agent reliability

The future system may use different models for different roles.

### 3. Intelligent Memory Retrieval

Current vector search can retrieve technically related but low-value notes.

Target architecture:

Qdrant Search
→ Candidate Memories
→ Memory Ranker / Reranker
→ Best Relevant Memories
→ Compression
→ LLM

### 4. True Memory Compression

The existing `MemoryCompressor` currently behaves more like a Context Builder.

Future compressor should:

* Remove repetitive ideas
* Retain query-relevant passages
* Reduce prompt size
* Reduce model latency
* Preserve source provenance

### 5. Pipeline Tests

Add automated tests for:

* Correct stage order
* State before memory
* State authority
* Router metadata
* Prompt versions
* Memory source uniqueness
* Correct prompt sections
* Error handling

### 6. LLM Planner

Replace the keyword-based Planner with a structured LLM planner.

Expected output should include fields such as:

* Primary role
* Specialists
* Needs memory
* Complexity
* Required tools
* Expected execution strategy

Planner output should be structured and validated.

### 7. Multi-Agent Execution

Allow multiple specialists to work on the same Task.

Example:

Planner
→ Developer + Research + CEO
→ Individual outputs
→ Critique / comparison
→ Combined final answer

---

## Future Autonomous Research System

A major future AI-OS capability will be persistent Research Sessions.

Example:

“Research the best startup I can build with €5,000 for the next 72 hours.”

Instead of answering once, AI-OS should continue researching autonomously until a deadline or convergence condition.

### Research Loop

Goal
→ Generate research questions
→ Search internet and local memory
→ Generate hypotheses and ideas
→ Challenge assumptions
→ Research missing information
→ Revise ideas
→ Rank/filter
→ Ask new questions
→ Repeat
→ Final synthesis

### Research Roles

Possible roles:

* Research Manager
* Explorer
* Researcher
* Ideator
* Critic / Skeptic
* Analyst
* Judge
* Final Synthesizer

The same underlying model may initially perform multiple roles using different prompts.

### Research Modes

* Autonomous
* Interactive
* Approval-gated

Autonomous mode should continue while the user is busy but still allow intervention.

### Internet

Research Sessions may use the internet automatically.

Internet activity should be controlled by resource limits rather than unlimited browsing.

Possible limits:

* Duration
* Concurrent tasks
* Pages per iteration
* Failed retries
* Disk quota
* Model runtime
* Search budget
* Domain restrictions

The system should optimize for **information gain**, not number of searches.

### Research Memory

Autonomous research should not dump all temporary thoughts into the permanent Second Brain.

Use three levels:

1. Working research memory
2. Research record
3. Curated long-term knowledge

Example workspace:

`vault/02-Research/Autonomous/<Research-Session>/`

Possible files:

* Overview.md
* Questions.md
* Ideas.md
* Evidence.md
* Rejected-Ideas.md
* Decisions.md
* Progress.md
* Final-Report.md

### Domain Profiles

Build one reusable autonomous research engine with specialized profiles.

Possible profiles:

* Generic
* Business
* Trading
* Academic Research

Business mode should allow broad creative brainstorming early and require more evidence as ideas approach finalist status.

Trading mode should be much stricter:

Hypothesis
→ Evidence
→ Backtest
→ Critic Review
→ Out-of-Sample Validation
→ Risk Analysis
→ Paper Trading

No trading strategy should be accepted merely because the model considers it promising.

---

## Future Integration Layer

Later AI-OS may expose tools through:

* MCP
* OpenAPI
* Local APIs

Potential consumers:

* Open WebUI
* Custom AI-OS dashboard
* Other AI clients
* Future agent systems

AI-OS should remain the core orchestration engine.

---

## Longer-Term Ideas

Future ideas should be implemented only when architecture and project maturity justify them.

Potential components:

### Event System

`brain/events/`

Possible future flow:

Planner finished
→ emit event
→ Router reacts
→ Memory reacts
→ Logger reacts

### Tool Registry

Central registry for:

* Web search
* Browser
* Files
* APIs
* Coding tools
* Database access
* Obsidian
* Research tools

### Agent Messaging

Enable specialist agents to communicate through structured Task state rather than free-form chat.

### Automatic State Updates

Eventually State may update automatically after:

* Successful milestones
* Tests
* Git commits
* Completed Research Sessions

Manual override must remain possible.

---

## Development Workflow

For every meaningful feature:

1. Inspect current code
2. Make a small Git-style patch
3. Compile
4. Run targeted test
5. Run integration test
6. Review `git diff`
7. Commit
8. Update documentation/state
9. Continue

Avoid large file replacements unless necessary.

---

## Current Next Step

The repository is currently clean at commit:

`b8deed2`

Before major Brain changes, create this status document and commit it.

After that:

**Begin the controlled Python 3.12 root-environment migration.**
