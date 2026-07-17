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

from brain.state.provider import StateProvider
from brain.memory.compression import MemoryCompressor
from brain.execution.task import Task
from brain.memory.search import MemorySearch
from brain.models.ollama import OllamaClient
from brain.planner.planner import Planner
from brain.router.router import SpecialistRouter


class ExecutionPipeline:
    def __init__(self):
        self.state = StateProvider()
        self.planner = Planner()
        self.router = SpecialistRouter()
        self.planner = Planner()
        self.router = SpecialistRouter()
        self.state = StateProvider()
        self.memory = MemorySearch()
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
        return task

    def run_routing(self, task: Task) -> Task:
        return self.router.route(task)
    def load_current_state(self, task: Task) -> Task:
        task.current_state = self.state.snapshot()
        task.state_context = self.state.format_context(
            task.current_state
        )

        task.metadata["state"] = {
            "version": task.current_state.get("version"),
            "current_focus": task.current_state.get("current_focus"),
            "next_focus": task.current_state.get("next_focus"),
        }

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
        if task.system_prompt is None:
            raise RuntimeError("System prompt was not loaded by the Router.")

        if task.specialist_prompt is None:
            raise RuntimeError("Specialist prompt was not loaded by the Router.")

        specialists = ", ".join(task.specialists) or task.primary_role or "general"

        task.prompt = f"""
    {task.system_prompt.content}

## Active Specialist

    {task.specialist_prompt.content}

## Execution Plan

- Primary role: {task.primary_role}
- Specialists involved: {specialists}

## Current Project State

    {task.state_context}

## Retrieved Memory

    {task.context}

## User Request

    {task.query}

Provide a clear and practical response.
""" .strip()

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
            self.run_routing(task)
            self.load_current_state(task)
            self.run_memory_retrieval(task, limit=memory_limit)
            self.build_context(task)
            self.build_prompt(task)
            self.run_model(task)
        except Exception as error:
            task.errors.append(f"{type(error).__name__}: {error}")

        self.collect_metadata(task, started_at)
        return task