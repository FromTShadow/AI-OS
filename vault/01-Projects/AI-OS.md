# AI-OS — Project Status

## Current Version

**v0.3.6-dev**

Latest milestone commit: `9861b6f` — Enable LLM planner by default and advance project state.

## Project Goal

AI-OS is a local-first, modular AI platform designed to coordinate local models, shared memory, specialist roles, and future multi-agent workflows.

Long-term goals include research automation, software development, knowledge management, and content and business automation.

## Current Architecture

User Request → Task → LLM Planner → Specialist Router → Current State → Qdrant Memory Retrieval → Context Builder → Prompt Builder → Ollama → Answer and Execution Metadata

**Core principle:** Current State represents the latest known reality. Historical memory provides context but must not override authoritative state.

## Implemented Components

- Docker-based supporting infrastructure
- Ollama model integration
- Execution pipeline and Task workflow
- LLM Planner with structured output, validation, retry, and fallback
- Specialist Router
- Current State provider
- Markdown-based role prompts and prompt loader
- Qdrant semantic memory retrieval
- Obsidian-to-Qdrant indexing and chunking
- Memory ranking and compression components
- Execution metadata and memory-source reporting
- Model benchmarking and evaluation tools

## Models

- `qwen3.5:4b` — configured LLM Planner model
- `qwen3:14b` — used for generation in a successful pipeline run
- `qwen3.5:9b` — benchmark candidate
- `nomic-embed-text` — embedding model

## Validation

- LLM Planner retry and fallback tests passed.
- Planner integration test passed.
- The end-to-end pipeline completed successfully.
- The successful run retrieved five memory sources and generated an answer.

A successful run does not guarantee factual correctness. Research grounding, response quality, memory quality, and dependency error handling remain areas for improvement.

## Current Development Focus

**Multi-agent execution preparation**

Next milestone: prototype coordinated specialist execution.

### Planned workflow

1. Planner creates a structured plan.
2. Assign tasks to appropriate specialists.
3. Collect individual specialist results.
4. Validate and critique the results.
5. Synthesize the final response.

## Development Principles

- Make small, reviewable changes.
- Keep current state separate from historical memory.
- Validate structured model outputs.
- Test components before integration.
- Preserve benchmark results and Git history.
- Document limitations honestly.

See `PROJECT_STATUS.md` for the detailed implementation status and `docs/ARCHIVED_PLANS_AND_ROADMAP.md` for preserved historical plans and long-term ideas.