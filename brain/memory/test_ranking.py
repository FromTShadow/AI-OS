from dataclasses import dataclass

from brain.memory.ranking import MemoryRanker


@dataclass
class FakeResult:
    score: float
    payload: dict


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

ranked = ranker.rank(
    query=query,
    results=results,
    limit=2,
)

print("Ranking:")
for result in ranked:
    print(
        result.payload["title"],
        "semantic=",
        result.score,
        "final=",
        round(ranker.score(query, result), 3),
    )

assert ranked[0].payload["title"] == "AI-OS"
assert ranked[1].payload["title"] == "Developer-Agent"

print("\nMemory Ranker test passed.")