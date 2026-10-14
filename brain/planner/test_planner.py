import pytest

from brain.planner.planner import Planner


@pytest.fixture
def planner():
    return Planner()


@pytest.mark.parametrize(
    "query",
    [
        "Build me a website for my AI OS",
        "Research best local AI models",
        "Organize my Obsidian notes",
        "Create a trading bot roadmap",
        "What should I prioritize next?",
    ],
)
def test_planner_classifies_queries(planner, query):
    plan = planner.classify(query)

    assert isinstance(plan, dict)
    assert "primary_role" in plan
    assert "needs" in plan
    assert isinstance(plan["needs"], dict)
