from brain.benchmarks.quality_v2 import QualityEvaluatorV2


evaluator = QualityEvaluatorV2()


good_reasoning = """
Model generation is the bottleneck.

Retrieval takes 0.6 seconds while model generation takes 80 seconds,
so generation should be optimized first.
"""


bad_reasoning = """
The model takes 80 seconds.

We should optimize performance.
"""


good_result = evaluator.evaluate(
    case_name="reasoning",
    response=good_reasoning,
)

bad_result = evaluator.evaluate(
    case_name="reasoning",
    response=bad_reasoning,
)


print("Good reasoning:")
print("Score:", good_result.score)
print("Passed:", good_result.passed_checks)
print("Failed:", good_result.failed_checks)

print()

print("Weak reasoning:")
print("Score:", bad_result.score)
print("Passed:", bad_result.passed_checks)
print("Failed:", bad_result.failed_checks)


assert good_result.score == 100.0

assert bad_result.score < 100.0

assert "uses_both_timings" in good_result.passed_checks

assert "uses_both_timings" in bad_result.failed_checks

assert (
    "correct_optimization_target"
    in bad_result.failed_checks
)

planning_v2 = """
The next priority should be the LLM Planner because it will improve
task decomposition before multi-agent execution is introduced.

After that, add pipeline tests before expanding the architecture.

Finally, implement multi-agent execution once the foundation is stable.
"""

planning_v2_result = evaluator.evaluate(
    case_name="planning_priorities",
    response=planning_v2,
)

print()
print("Planning V2:")
print("Score:", planning_v2_result.score)
print("Passed:", planning_v2_result.passed_checks)
print("Failed:", planning_v2_result.failed_checks)

assert planning_v2_result.score == 100.0
assert "mentions_llm_planner" in planning_v2_result.passed_checks
assert "mentions_multi_agent" in planning_v2_result.passed_checks


print("\nQuality Evaluator V2 test passed.")