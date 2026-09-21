"""
Regression test for the AIBrain compatibility adapter.

Uses a fake pipeline so the test is fast and does not call Ollama,
Qdrant, or other external services.
"""

from brain.core.brain import AIBrain
from brain.execution.task import Task


class FakePipeline:
    def __init__(self):
        self.calls = []

    def execute(
        self,
        query: str,
        memory_limit: int = 5,
    ) -> Task:
        self.calls.append(
            {
                "query": query,
                "memory_limit": memory_limit,
            }
        )

        task = Task(query=query)
        task.answer = "Adapter response."
        task.plan = {
            "needs": {
                "memory": True,
            }
        }
        task.current_state = {
            "version": "0.3.4-dev",
            "current_focus": "Pipeline testing and observability",
            "next_focus": "LLM Planner preparation",
        }
        task.primary_role = "research"
        task.specialists = ["research"]

        return task


pipeline = FakePipeline()
brain = AIBrain(pipeline=pipeline)

response = brain.answer(
    "Test authoritative state",
    memory_limit=3,
)

assert pipeline.calls == [
    {
        "query": "Test authoritative state",
        "memory_limit": 3,
    }
]

assert "Adapter response." in response
assert "Primary role: research" in response
assert "Version: 0.3.4-dev" in response
assert "Pipeline testing and observability" in response
assert "LLM Planner preparation" in response
assert "No memory sources used." in response

print("AIBrain pipeline adapter test passed.")