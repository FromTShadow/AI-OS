"""
AI-OS Model Benchmark V3.

V3 evaluates structured model outputs instead of relying mainly
on keyword matching.

Initial proof-of-concept cases:
- planning
- reasoning
"""

from dataclasses import dataclass
from typing import List


@dataclass
class BenchmarkCaseV3:
    name: str
    category: str
    prompt: str


class BenchmarkCasesV3:
    def cases(self) -> List[BenchmarkCaseV3]:
        return [
            BenchmarkCaseV3(
                name="planning_priorities_structured",
                category="planning",
                prompt="""
You are planning development of a local AI operating system.

Current state:
- Memory system: complete
- Specialist router: complete
- Current-state system: complete
- Pipeline observability: complete
- Model benchmarking: in progress
- LLM Planner: not built
- Multi-agent execution: not built
- Autonomous research sessions: future goal

Return ONLY valid JSON using exactly this structure:

{
  "priorities": [
    {
      "rank": 1,
      "name": "string",
      "rationale": "string",
      "dependencies": ["string"],
      "tradeoffs": ["string"]
    },
    {
      "rank": 2,
      "name": "string",
      "rationale": "string",
      "dependencies": ["string"],
      "tradeoffs": ["string"]
    },
    {
      "rank": 3,
      "name": "string",
      "rationale": "string",
      "dependencies": ["string"],
      "tradeoffs": ["string"]
    }
  ]
}

Choose the three highest-priority next development steps.
Do not include Markdown or text outside the JSON.
""".strip(),
            ),

                        BenchmarkCaseV3(
                name="reasoning_bottleneck_structured",
                category="reasoning",
                prompt="""
An AI pipeline has these measured timings:

planning_seconds = 0.5
retrieval_seconds = 0.7
context_seconds = 0.2
generation_seconds = 75.0

Return ONLY valid JSON using exactly this structure:

{
  "bottleneck": "string",
  "bottleneck_seconds": 0.0,
  "optimize_first": "string",
  "reason": "string"
}

Identify the dominant bottleneck and which component should be optimized first.

Do not include Markdown or text outside the JSON.
""".strip(),
            ),

            BenchmarkCaseV3(
                name="coding_remove_duplicates_executable",
                category="coding",
                prompt="""
Write Python code that defines exactly this function:

def remove_duplicates(items: list[str]) -> list[str]:

Requirements:
- Remove duplicate strings
- Preserve original order
- Do not mutate the input list
- Include type annotations
- Return only valid Python code
- Do not include Markdown fences
- Do not include explanation text
""".strip(),
            ),
            BenchmarkCaseV3(
                name="coding_normalize_scores_debug",
                category="coding",
                prompt="""
The following function is buggy:

def normalize_scores(scores: list[float]) -> list[float]:
    scores.sort()

    maximum = max(scores)

    return [
        score / maximum
        for score in scores
    ]

Repair the function.

Requirements:
- Function name must remain normalize_scores
- Input type: list[float]
- Return type: list[float]
- Do not mutate the input list
- Preserve original element order
- Normalize values to the range 0.0 to 1.0 using min-max normalization
- The minimum input value must map to 0.0
- The maximum input value must map to 1.0
- For an empty list, return []
- If all values are equal, return a list of 0.0 values of the same length
- Support negative values
- Return only valid Python code
- Do not include Markdown fences
- Do not include explanation text
""".strip(),
),
        ]
