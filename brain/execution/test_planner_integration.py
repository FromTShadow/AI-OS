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
            "steps": ["Create a structured plan."],
            "risks": ["The benchmark may use stale assumptions."],
            "success_criteria": ["Planner metadata is recorded."],
            "planner_type": "llm",
            "planner_attempts": 2,
            "fallback_reason": None,
        }


def test_planner_injection_and_prompt_observability():
    planner = FakePlanner()
    pipeline = ExecutionPipeline(planner=planner)
    task = Task(query="Research and build a benchmark.")

    task = pipeline.run_planning(task)

    assert planner.calls == ["Research and build a benchmark."]
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

    expected_sections = [
        "## Authoritative Current Project State",
        "## Structured Execution Plan",
        "## Historical Project Memory",
        "## User Request",
    ]

    for section in expected_sections:
        assert section in task.prompt

    expected_content = [
        "Test Pipeline planner integration.",
        "Create a structured plan.",
        "The benchmark may use stale assumptions.",
        "Planner metadata is recorded.",
        "Historical test context.",
        "Research and build a benchmark.",
    ]

    for content in expected_content:
        assert content in task.prompt

    positions = [
        task.prompt.index(section)
        for section in expected_sections
    ]
    assert positions == sorted(positions)


def test_format_execution_plan_legacy_fallback():
    pipeline = ExecutionPipeline()
    task = Task(query="Fallback compatibility test.")

    task.plan = {
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

    plan_text = pipeline.format_execution_plan(task)

    assert "Fallback compatibility test." in plan_text
    assert plan_text.count("- None provided.") == 3