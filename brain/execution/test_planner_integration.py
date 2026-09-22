"""
Tests planner injection and planner observability in the Pipeline.

The fake planner avoids real model calls.
"""

from brain.execution.pipeline import ExecutionPipeline
from brain.execution.task import Task


class FakePlanner:
    def __init__(self):
        self.model = "fake-planner-model"
        self.calls = []

    def classify(self, query: str):
        self.calls.append(query)

        return {
            "query": query,
            "needs": {
                "memory": True,
                "developer": True,
                "research": True,
                "second_brain": False,
                "trading": False,
                "ceo": False,
            },
            "primary_role": "research",
            "goal": "Test Pipeline planner integration.",
            "steps": [
                "Create a structured plan.",
            ],
            "risks": [],
            "success_criteria": [
                "Planner metadata is recorded.",
            ],
            "planner_type": "llm",
            "planner_attempts": 2,
            "fallback_reason": None,
        }


planner = FakePlanner()
pipeline = ExecutionPipeline(planner=planner)
task = Task(query="Research and build a benchmark.")

task = pipeline.run_planning(task)

assert planner.calls == [
    "Research and build a benchmark."
]
assert task.plan["primary_role"] == "research"
assert task.plan["needs"]["developer"] is True
assert task.plan["needs"]["research"] is True

planner_metadata = task.metadata["planner"]

assert planner_metadata["implementation"] == "FakePlanner"
assert planner_metadata["planner_type"] == "llm"
assert planner_metadata["model"] == "fake-planner-model"
assert planner_metadata["attempts"] == 2
assert planner_metadata["fallback_reason"] is None

print("Pipeline planner integration test passed.")