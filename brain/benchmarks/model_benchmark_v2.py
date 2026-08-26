"""
AI-OS Model Benchmark V2.

Uses harder, more realistic AI-OS tasks with multiple cases
per capability category.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class BenchmarkCaseV2:
    name: str
    category: str
    prompt: str


class BenchmarkCasesV2:
    def cases(self) -> List[BenchmarkCaseV2]:
        return [
            # -------------------------
            # PLANNING
            # -------------------------
            BenchmarkCaseV2(
                name="planning_priorities",
                category="planning",
                prompt=(
                    "You are managing development of a local AI operating "
                    "system. The memory system works, the router works, and "
                    "pipeline observability works. The LLM planner and "
                    "multi-agent execution are not built yet. Identify the "
                    "three highest-priority next steps and explain the order."
                ),
            ),
            BenchmarkCaseV2(
                name="planning_conflict",
                category="planning",
                prompt=(
                    "A local AI project has limited developer time. You can "
                    "either improve model quality, add multi-agent execution, "
                    "or build more automated tests. The system is functional "
                    "but still changing quickly. Decide what should come first "
                    "and explain the trade-offs."
                ),
            ),
            BenchmarkCaseV2(
                name="planning_architecture",
                category="planning",
                prompt=(
                    "Design the next development phase for a modular local AI "
                    "system that already has planning, routing, memory, state, "
                    "and model execution. Prioritize architecture that makes "
                    "future autonomous research sessions easier to build."
                ),
            ),

            # -------------------------
            # CODING
            # -------------------------
            BenchmarkCaseV2(
                name="coding_implementation",
                category="coding",
                prompt=(
                    "Write a production-quality Python function that accepts "
                    "a list of strings and returns them without duplicates "
                    "while preserving original order. Include type hints and "
                    "briefly explain time complexity."
                ),
            ),
            BenchmarkCaseV2(
                name="coding_debugging",
                category="coding",
                prompt=(
                    "This Python function is supposed to return unique strings "
                    "in original order, but it returns an unordered result:\n\n"
                    "def unique(items: list[str]) -> list[str]:\n"
                    "    return list(set(items))\n\n"
                    "Explain the bug and provide a corrected implementation "
                    "with type hints."
                ),
            ),
            BenchmarkCaseV2(
                name="coding_architecture",
                category="coding",
                prompt=(
                    "A Python AI pipeline currently passes many unrelated "
                    "arguments between stages. Propose a maintainable "
                    "refactor using a shared Task or ExecutionContext object. "
                    "Show a small code example and discuss one trade-off."
                ),
            ),

            # -------------------------
            # RESEARCH
            # -------------------------
            BenchmarkCaseV2(
                name="research_comparison",
                category="research",
                prompt=(
                    "Compare vector search, keyword search, and hybrid search "
                    "for a local AI knowledge system. Explain strengths, "
                    "weaknesses, and when each approach is appropriate."
                ),
            ),
            BenchmarkCaseV2(
                name="research_synthesis",
                category="research",
                prompt=(
                    "A local AI system retrieves semantically similar notes, "
                    "but many are technically relevant and practically useless. "
                    "Explain at least three methods that could improve retrieval "
                    "quality and how they could be combined."
                ),
            ),
            BenchmarkCaseV2(
                name="research_uncertainty",
                category="research",
                prompt=(
                    "Two benchmark runs disagree: Model A is faster overall, "
                    "while Model B performs better on one important coding task. "
                    "Explain how you would evaluate which model should be used "
                    "in production without overclaiming from limited evidence."
                ),
            ),

            # -------------------------
            # REASONING
            # -------------------------
            BenchmarkCaseV2(
                name="reasoning_bottleneck",
                category="reasoning",
                prompt=(
                    "An AI request takes 0.5 seconds for planning, 0.7 seconds "
                    "for retrieval, 0.2 seconds for context building, and "
                    "75 seconds for model generation. Identify the main "
                    "bottleneck and explain what should be optimized first."
                ),
            ),
            BenchmarkCaseV2(
                name="reasoning_constraints",
                category="reasoning",
                prompt=(
                    "You have 24 GB unified memory. Model A uses 6 GB and takes "
                    "30 seconds. Model B uses 14 GB and takes 45 seconds but is "
                    "more accurate. Docker services typically consume another "
                    "5 GB. Explain which model is safer as the default and when "
                    "the larger model might still be appropriate."
                ),
            ),
            BenchmarkCaseV2(
                name="reasoning_tradeoff",
                category="reasoning",
                prompt=(
                    "A smaller AI model scores 90% quality and finishes in "
                    "20 seconds. A larger model scores 100% quality and takes "
                    "60 seconds. Explain how you would choose between them for "
                    "planning, coding, and deep research workloads."
                ),
            ),
        ]