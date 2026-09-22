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
            "risks": [
                "The benchmark may use stale assumptions.",
            ],
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

task = pipeline.run_routing(task)
task = pipeline.load_current_state(task)
task.context = "Historical test context."
task = pipeline.build_prompt(task)

assert "## Authoritative Current Project State" in task.prompt
assert "## Structured Execution Plan" in task.prompt
assert "## Historical Project Memory" in task.prompt
assert "## User Request" in task.prompt

assert "Test Pipeline planner integration." in task.prompt
assert "Create a structured plan." in task.prompt
assert "The benchmark may use stale assumptions." in task.prompt
assert "Planner metadata is recorded." in task.prompt
assert "Historical test context." in task.prompt
assert "Research and build a benchmark." in task.prompt

state_position = task.prompt.index(
    "## Authoritative Current Project State"
)
plan_position = task.prompt.index(
    "## Structured Execution Plan"
)
memory_position = task.prompt.index(
    "## Historical Project Memory"
)
request_position = task.prompt.index(
    "## User Request"
)

assert state_position < plan_position
assert plan_position < memory_position
assert memory_position < request_position


fallback_task = Task(
    query="Fallback compatibility test."
)
fallback_task.plan = {
    "needs": {
        "memory": True,
        "developer": False,
        "research": False,
        "second_brain": False,
        "trading": False,
        "ceo": True,
    },
    "primary_role": "ceo",
}

fallback_plan_text = pipeline.format_execution_plan(
    fallback_task
)

assert "Fallback compatibility test." in fallback_plan_text
assert fallback_plan_text.count("- None provided.") == 3

print("Pipeline planner integration test passed.")