"""
Compatibility interface for the AI-OS execution pipeline.

AIBrain preserves the original answer() interface while delegating all
planning, routing, state loading, memory handling, prompt construction,
and model execution to ExecutionPipeline.
"""

from brain.execution.pipeline import ExecutionPipeline
from brain.execution.task import Task


class AIBrain:
    def __init__(
        self,
        pipeline: ExecutionPipeline | None = None,
    ):
        self.pipeline = pipeline or ExecutionPipeline()

    def execute(
        self,
        query: str,
        memory_limit: int = 5,
    ) -> Task:
        return self.pipeline.execute(
            query,
            memory_limit=memory_limit,
        )

    def format_plan(self, task: Task) -> str:
        specialists = ", ".join(task.specialists) or (
            task.primary_role or "general"
        )
        needs_memory = task.plan.get("needs", {}).get(
            "memory",
            True,
        )

        return (
            f"Primary role: {task.primary_role or 'general'}\n"
            f"Specialists needed: {specialists}\n"
            f"Memory needed: {needs_memory}"
        )

    def format_state(self, task: Task) -> str:
        state = task.current_state

        return (
            f"Version: {state.get('version', 'unknown')}\n"
            f"Current focus: "
            f"{state.get('current_focus', 'unknown')}\n"
            f"Next focus: {state.get('next_focus', 'unknown')}"
        )

    def format_sources(self, task: Task) -> str:
        if not task.memory_results:
            return "No memory sources used."

        lines = []

        for index, result in enumerate(
            task.memory_results,
            start=1,
        ):
            payload = result.payload or {}
            title = payload.get("title", "Untitled")
            folder = payload.get("folder", "Unknown")
            chunk_index = payload.get("chunk_index", 0)
            score = round(result.score, 3)

            lines.append(
                f"{index}. {title} | "
                f"folder: {folder} | "
                f"chunk: {chunk_index} | "
                f"score: {score}"
            )

        return "\n".join(lines)

    def format_response(self, task: Task) -> str:
        return (
            f"{task.answer}\n\n"
            f"---\n"
            f"Brain plan:\n{self.format_plan(task)}\n\n"
            f"Authoritative state:\n{self.format_state(task)}\n\n"
            f"Memory sources used:\n{self.format_sources(task)}"
        )

    def answer(
        self,
        query: str,
        memory_limit: int = 5,
    ) -> str:
        task = self.execute(
            query,
            memory_limit=memory_limit,
        )

        if task.errors:
            details = "; ".join(task.errors)
            raise RuntimeError(
                f"AI Brain pipeline failed: {details}"
            )

        return self.format_response(task)