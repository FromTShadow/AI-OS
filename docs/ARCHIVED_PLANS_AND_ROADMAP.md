# AI-OS --- Archived Plans and Roadmap

> **Purpose:** Preserve the plans and architectural ideas from the
> earlier `PROJECT_STATUS.md` before that file was consolidated.
>
> **Status note:** This is an archive of previously documented plans,
> not a claim that every item remains current. Some items---especially
> the Python environment migration and LLM Planner---were later
> completed. Check `brain/state/current.py` and the current
> `PROJECT_STATUS.md` before treating an item as active work.

## 1. Near-Term Engineering Roadmap from the Earlier Status Document

### 1.1 Modern Python Environment Migration --- Historical Plan

The earlier plan was to move AI-OS to a root-level Python environment
and avoid removing the old environment until validation was complete.

The migration checklist was:

-   Create `~/AI-OS/.venv`.
-   Install dependencies.
-   Test configuration.
-   Test Ollama.
-   Test Qdrant.
-   Test memory search.
-   Test indexing.
-   Test Planner.
-   Test Router.
-   Test State Provider.
-   Test Prompt Loader.
-   Test Execution Pipeline.
-   Run an end-to-end Brain test.
-   Verify Open WebUI integrations.
-   Verify PostgreSQL.
-   Verify n8n.
-   Commit the migration.
-   Remove the old virtual environment only after all tests pass.

**Historical outcome:** Later project notes reported that the root
environment was migrated to Python 3.13.15 and end-to-end validation
completed. Treat this checklist as historical unless a future
environment migration is needed.

### 1.2 Local Model Benchmarking

Do not replace `qwen3:14b` solely because a newer model is available.
Benchmark candidate models against actual AI-OS workloads.

Evaluation criteria from the earlier plan:

-   Planning accuracy.
-   Coding quality.
-   Tool use.
-   Research reasoning.
-   Memory-grounded answers.
-   Speed and latency.
-   RAM usage.
-   Reliability during long-running agent tasks.

The system may eventually use different models for different roles
rather than one model for everything.

### 1.3 Intelligent Memory Retrieval

The earlier plan noted that vector search could retrieve notes that were
technically related but not useful enough for the current task.

Proposed flow:

1.  Qdrant search.
2.  Retrieve candidate memories.
3.  Rank or rerank candidates.
4.  Select the most relevant memories.
5.  Compress or curate the selected context.
6.  Pass the context to the model.

Goals:

-   Improve relevance, not just semantic similarity.
-   Reduce repetitive or low-value context.
-   Preserve source provenance.
-   Avoid allowing historical memory to override authoritative current
    state.

### 1.4 True Memory Compression

The earlier document noted that the existing `MemoryCompressor` behaved
more like a context builder than a true compressor.

Potential responsibilities for a more complete compressor:

-   Remove repetitive ideas.
-   Retain query-relevant passages.
-   Reduce prompt size.
-   Reduce model latency.
-   Preserve source provenance.

Compression should be evaluated for information loss and factual
consistency, not only for how much text it removes.

### 1.5 Pipeline Tests

The earlier plan called for tests covering:

-   Correct pipeline stage order.
-   Current state being included before historical memory.
-   Current-state authority.
-   Router metadata.
-   Prompt versions.
-   Memory-source uniqueness.
-   Correct prompt sections.
-   Dependency and stage error handling.

These should be treated as test targets to verify against the current
test suite; this archive does not assert that every item has been
implemented.

### 1.6 LLM Planner --- Historical Plan

The earlier roadmap proposed replacing the keyword-based Planner with a
structured LLM Planner.

Expected structured output included:

-   Primary role.
-   Specialist roles.
-   Whether memory is needed.
-   Task complexity.
-   Required tools.
-   Expected execution strategy.

Planner output should be structured and validated.

**Historical outcome:** The LLM Planner was later implemented with
structured output, validation, retry, and fallback behavior, and was
configured as the default planner. Future work should focus on observed
planning failures and evaluation rather than repeating the original
implementation task.

### 1.7 Multi-Agent Execution

Allow multiple specialists to work on a single task while coordinating
through structured data rather than unstructured, free-form
conversation.

Earlier example:

1.  Planner.
2.  Assign work to Developer, Research, and/or CEO specialists.
3.  Collect individual outputs.
4.  Critique or compare results.
5.  Synthesize a combined final answer.

A more explicit proposed workflow is:

1.  Planner creates a task plan.
2.  Assign specialist tasks with clear inputs and expected outputs.
3.  Execute specialist tasks.
4.  Validate individual results.
5.  Critique, compare, or resolve disagreements.
6.  Synthesize a final result.
7.  Return the response with execution metadata and relevant provenance.

Potential design concerns to address when implementing this:

-   Task and result schemas.
-   Dependencies between specialist tasks.
-   Failure, retry, and timeout behavior.
-   Duplicate or conflicting work.
-   Validation and evidence requirements.
-   Resource limits and cancellation.
-   Human approval for consequential actions.
-   Traceability of each specialist's contribution.

## 2. Future Autonomous Research System

A major long-term idea was persistent **Research Sessions**: instead of
answering once, AI-OS would keep researching toward a goal until a
deadline, resource limit, or convergence condition is reached.

Example goal from the earlier notes:

> "Research the best startup I can build with €5,000 for the next 72
> hours."

This is an example of the intended interaction, not a commitment to run
research continuously for that duration.

### 2.1 Proposed Research Loop

1.  Define the goal and constraints.
2.  Generate research questions.
3.  Search the internet and local memory.
4.  Generate hypotheses and ideas.
5.  Challenge assumptions.
6.  Identify missing information.
7.  Research the gaps.
8.  Revise hypotheses and ideas.
9.  Rank and filter candidate conclusions.
10. Generate follow-up questions.
11. Repeat while useful and within limits.
12. Produce a final synthesis with evidence, uncertainty, and
    recommendations.

The system should optimize for **information gain**, not simply the
number of searches or pages visited.

### 2.2 Possible Research Roles

-   **Research Manager:** Maintains the goal, task queue, and progress.
-   **Explorer:** Finds broad directions and potentially useful sources.
-   **Researcher:** Investigates specific questions.
-   **Ideator:** Generates candidate hypotheses or solutions.
-   **Critic / Skeptic:** Challenges assumptions and searches for
    counterevidence.
-   **Analyst:** Compares evidence and evaluates candidates.
-   **Judge:** Applies explicit criteria to rank or filter candidates.
-   **Final Synthesizer:** Produces the final report.

The same underlying model could initially perform multiple roles using
different prompts. Separate models may be introduced if benchmarks
justify the added complexity.

### 2.3 Research Modes

Possible modes:

-   **Autonomous:** Continue without requiring approval for each
    research iteration, within configured limits.
-   **Interactive:** Ask the user questions and accept direction during
    the session.
-   **Approval-gated:** Pause for approval at defined decision points.

Autonomous operation should still allow the user to inspect progress,
intervene, and stop a session.

### 2.4 Internet Access and Resource Limits

Research Sessions may use internet search automatically, but access
should be governed by explicit limits rather than being unlimited.

Potential limits:

-   Maximum session duration.
-   Maximum concurrent tasks.
-   Maximum pages per iteration.
-   Maximum failed retries.
-   Disk quota.
-   Model runtime or token budget.
-   Search budget.
-   Allowed or blocked domains.

Research outputs should distinguish source-backed facts, hypotheses,
inferences, and unresolved questions.

### 2.5 Research Memory

Temporary research thoughts should not automatically be dumped into
permanent Second Brain memory.

Proposed three-level memory structure:

1.  **Working research memory:** Temporary notes, questions, candidate
    ideas, and intermediate results.
2.  **Research record:** Persistent session history, evidence, rejected
    ideas, decisions, and progress.
3.  **Curated long-term knowledge:** Verified or useful conclusions
    selected for the permanent knowledge base.

Earlier proposed workspace:

`vault/02-Research/Autonomous/<Research-Session>/`

Possible files:

-   `Overview.md`
-   `Questions.md`
-   `Ideas.md`
-   `Evidence.md`
-   `Rejected-Ideas.md`
-   `Decisions.md`
-   `Progress.md`
-   `Final-Report.md`

The session should preserve source links and enough provenance to
revisit important conclusions.

### 2.6 Domain Profiles

The idea was to build one reusable autonomous research engine with
specialized profiles.

Possible profiles:

-   Generic research.
-   Business research.
-   Trading research.
-   Academic research.

**Business profile:** Permit broad creative exploration early, then
require stronger evidence and more rigorous comparison as ideas approach
finalist status.

**Trading profile:** Apply stricter evidence and validation
requirements. The earlier proposed process was:

Hypothesis → Evidence → Backtest → Critic Review → Out-of-Sample
Validation → Risk Analysis → Paper Trading

A trading strategy should not be accepted merely because a model
considers it promising. It needs reproducible testing, risk analysis,
and independent validation.

## 3. Future Integration Layer

AI-OS should remain the core orchestration engine rather than becoming
tightly coupled to a particular user interface.

Potential interfaces and integration methods:

-   MCP.
-   OpenAPI.
-   Local APIs.

Potential consumers:

-   Open WebUI.
-   A custom AI-OS dashboard.
-   Other AI clients.
-   Future agent systems.

The earlier design preference was to favor API-based integration and
standard interfaces over tight coupling to legacy Open WebUI Pipeline
plugins.

## 4. Longer-Term Architectural Ideas

These were ideas for later consideration, not requirements for the next
milestone. Implement them only when the architecture and project
maturity justify them.

### 4.1 Event System

Possible location:

`brain/events/`

Potential event flow:

1.  Planner finishes.
2.  Planner emits a structured event.
3.  Router reacts if needed.
4.  Memory components react if needed.
5.  Logging and observability record the event.

The event system should have clear event schemas, predictable error
handling, and safeguards against accidental repeated or circular
execution.

### 4.2 Tool Registry

A central registry could describe available tools, their input and
output schemas, permissions, and execution constraints.

Potential tool categories:

-   Web search.
-   Browser.
-   Files.
-   APIs.
-   Coding tools.
-   Database access.
-   Obsidian.
-   Research tools.

Tool access should be explicit and permission-aware. A tool should not
be exposed to every agent by default simply because it exists.

### 4.3 Agent Messaging

Enable specialists to communicate through structured task state and
typed results rather than relying exclusively on free-form chat.

This should make handoffs, validation, retries, and execution tracing
easier to reason about.

### 4.4 Automatic State Updates

In the future, project state might be updated after events such as:

-   Successful milestones.
-   Tests.
-   Git commits.
-   Completed Research Sessions.

Manual override must remain possible. Automatic updates should be based
on verifiable evidence and should not silently turn planned work into
completed work.

## 5. Earlier Architectural Decisions Worth Preserving

### 5.1 Task-Based Architecture

Pipeline components should increasingly accept and return a shared Task
object.

Target style:

``` python
task = stage.process(task)
```

The goal is to avoid long parameter lists and make future orchestration
easier. The earlier notes also raised the possibility of eventually
renaming `Task` to `ExecutionContext`; this was a future idea, not a
decision that the rename must happen.

### 5.2 Current State vs. Historical Memory

The earlier priority order was:

1.  Current State.
2.  Execution and Planner information.
3.  Historical memory.

Current State represents the latest known reality. Historical memory
provides context but must not override authoritative current state.

### 5.3 Prompt Architecture

Prompts should be stored as versioned Markdown files rather than
embedded as hardcoded Python strings.

Earlier prompt types included:

-   System.
-   Developer.
-   Research.
-   Second Brain.
-   Trading.
-   CEO.

### 5.4 Independence from Open WebUI

Open WebUI should be treated as a frontend/interface, not as the core
AI-OS architecture. The orchestration engine should remain usable
through other clients and interfaces.

## 6. Earlier Development Workflow

For every meaningful feature:

1.  Inspect the current code.
2.  Make a small, reviewable patch.
3.  Compile or perform relevant static checks.
4.  Run the targeted test.
5.  Run the integration test where appropriate.
6.  Review `git diff`.
7.  Commit the change.
8.  Update documentation and project state.
9.  Continue to the next increment.

Avoid large file replacements unless necessary. Preserve benchmark
results and Git history, and document limitations honestly.

## 7. Suggested Use of This Archive

-   Keep `PROJECT_STATUS.md` focused on the current implementation,
    current validation, known limitations, and next milestone.
-   Use this document to preserve older plans and ideas without
    presenting them as active work.
-   Before implementing any archived item, verify the current code and
    tests.
-   When an item is completed, record evidence of completion in the
    current status or relevant technical documentation.
-   Remove or revise archived ideas only when there is a deliberate
    decision to retire them.
