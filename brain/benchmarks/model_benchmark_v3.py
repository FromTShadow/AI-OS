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
        ]