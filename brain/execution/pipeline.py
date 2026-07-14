"""
Execution pipeline for AI-OS Brain.

Current flow:
Task
→ Planner
→ Memory retrieval
→ Context construction
→ Prompt construction
→ Ollama generation

Future stages will add:
- memory compression
- specialist routing
- multi-agent execution
- result review
"""

from time import perf_counter
from typing import Any, List

from brain.memory.compression import MemoryCompressor
from brain.execution.task import Task
from brain.memory.search import MemorySearch
from brain.models.ollama import OllamaClient
from brain.planner.planner import Planner


class ExecutionPipeline:
    def __init__(self):
        self.planner = Planner()
        self.memory = MemorySearch()
        self.compressor = MemoryCompressor()
        self.ollama = OllamaClient()

    def create_task(self, query: str) -> Task:
        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("Query cannot be empty.")

        return Task(query=cleaned_query)

    def run_planning(self, task: Task) -> Task:
        task.plan = self.planner.classify(task.query)
        task.primary_role = task.plan["primary_role"]

        needs = task.plan.get("needs", {})

        task.specialists = [
            role
            for role, is_needed in needs.items()
            if is_needed and role != "memory"
        ]

        return task

    def run_memory_retrieval(self, task: Task, limit: int = 5) -> Task:
        needs_memory = task.plan.get("needs", {}).get("memory", True)

        if not needs_memory:
            task.memory_results = []
            return task

        task.memory_results = self.memory.search(
            task.query,
            limit=limit,
        )

        return task

    def build_context(self, task: Task) -> Task:
        compressed = self.compressor.compress(
            query=task.query,
            results=task.memory_results,
        )

        task.context = compressed.context

        task.metadata["retrieved_memory_count"] = len(
            task.memory_results
        )
        task.metadata["compressed_source_count"] = (
            compressed.source_count
        )
        task.metadata["memory_original_characters"] = (
            compressed.original_characters
        )
        task.metadata["memory_compressed_characters"] = (
            compressed.compressed_characters
        )

        return task

    def build_prompt(self, task: Task) -> Task:
        specialists = ", ".join(task.specialists) or task.primary_role or "general"

        task.prompt = f"""
You are the AI Brain for Nejc's local AI Operating System.

Execution plan:
- Primary role: {task.primary_role}
- Specialists involved: {specialists}

Role guidance:
- developer: practical implementation, architecture, and production-quality code
- research: structured research, comparisons, evidence, and uncertainty
- second_brain: Obsidian organization, knowledge management, and useful links
- trading: systematic testing, data, automation, and risk management
- ceo: priorities, roadmaps, trade-offs, ROI, and avoiding overengineering

Use the retrieved memory only when relevant.
Do not pretend the memory contains information that is not present.
Clearly identify important missing information when necessary.

Memory context:
{task.context}

User request:
{task.query}

Provide a clear and practical response.
""".strip()

        return task

    def run_model(self, task: Task) -> Task:
        task.answer = self.ollama.chat(task.prompt)
        return task

    def collect_metadata(self, task: Task, started_at: float) -> Task:
        task.metadata["duration_seconds"] = round(
            perf_counter() - started_at,
            3,
        )
        task.metadata["memory_count"] = len(task.memory_results)
        task.metadata["primary_role"] = task.primary_role
        task.metadata["specialists"] = task.specialists

        return task

    def execute(self, query: str, memory_limit: int = 5) -> Task:
        started_at = perf_counter()
        task = self.create_task(query)

        try:
            self.run_planning(task)
            self.run_memory_retrieval(task, limit=memory_limit)
            self.build_context(task)
            self.build_prompt(task)
            self.run_model(task)
        except Exception as error:
            task.errors.append(f"{type(error).__name__}: {error}")

        self.collect_metadata(task, started_at)
        return task