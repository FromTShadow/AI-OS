from brain.benchmarks.quality_v3 import QualityEvaluatorV3


evaluator = QualityEvaluatorV3()


planning_response = """
{
  "priorities": [
    {
      "rank": 1,
      "name": "Improve benchmark quality",
      "rationale": "Reliable evaluation is needed before model routing.",
      "dependencies": [],
      "tradeoffs": ["Delays feature development"]
    },
    {
      "rank": 2,
      "name": "Build LLM Planner",
      "rationale": "Structured planning enables better orchestration.",
      "dependencies": ["Reliable model selection"],
      "tradeoffs": ["Adds another model call"]
    },
    {
      "rank": 3,
      "name": "Build multi-agent execution",
      "rationale": "Specialists can collaborate on complex tasks.",
      "dependencies": ["LLM Planner"],
      "tradeoffs": ["Higher complexity"]
    }
  ]
}
""".strip()


reasoning_response = """
{
  "bottleneck": "model_generation",
  "bottleneck_seconds": 75.0,
  "optimize_first": "model_generation",
  "reason": "Generation dominates the measured request latency."
}
""".strip()


planning_result = evaluator.evaluate(
    "planning_priorities_structured",
    planning_response,
)

reasoning_result = evaluator.evaluate(
    "reasoning_bottleneck_structured",
    reasoning_response,
)


print("Planning score:", planning_result.score)
print("Planning passed:", planning_result.passed_checks)
print("Planning failed:", planning_result.failed_checks)

print()

print("Reasoning score:", reasoning_result.score)
print("Reasoning passed:", reasoning_result.passed_checks)
print("Reasoning failed:", reasoning_result.failed_checks)


assert planning_result.score == 100.0
assert reasoning_result.score == 100.0


invalid_result = evaluator.evaluate(
    "reasoning_bottleneck_structured",
    "This is not JSON.",
)

assert invalid_result.score == 0.0
assert "valid_json" in invalid_result.failed_checks


print("\nQuality Evaluator V3 test passed.")