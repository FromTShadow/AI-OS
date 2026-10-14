from dataclasses import dataclass

from brain.memory.ranking import MemoryRanker


@dataclass
class FakeResult:
    score: float
    payload: dict


def test_memory_ranker_orders_project_context_first():
    ranker = MemoryRanker()
    query = "What should I prioritize next in my AI-OS project?"

    results = [
        FakeResult(
            score=0.68,
            payload={
                "title": "Developer-Agent",
                "folder": "07-AI-Agents",
                "content": (
                    "Developer specialist responsibilities, Python, "
                    "architecture, APIs, Docker, and implementation."
                ),
            },
        ),
        FakeResult(
            score=0.61,
            payload={
                "title": "AI-OS",
                "folder": "01-Projects",
                "content": (
                    "AI-OS project roadmap, current modules, priorities, "
                    "architecture, and next development steps."
                ),
            },
        ),
    ]

    ranked = ranker.rank(query=query, results=results, limit=2)

    assert len(ranked) == 2
    assert ranked[0].payload["title"] == "AI-OS"
    assert ranked[1].payload["title"] == "Developer-Agent"


def test_memory_ranker_respects_limit():
    ranker = MemoryRanker()
    query = "AI-OS project priorities"

    results = [
        FakeResult(
            score=0.8,
            payload={"title": "First", "content": "Project priorities"},
        ),
        FakeResult(
            score=0.7,
            payload={"title": "Second", "content": "Project roadmap"},
        ),
    ]

    ranked = ranker.rank(query=query, results=results, limit=1)

    assert len(ranked) == 1
