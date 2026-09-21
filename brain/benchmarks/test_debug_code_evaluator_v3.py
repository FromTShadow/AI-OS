from brain.benchmarks.debug_code_evaluator_v3 import (
    DebugCodeEvaluatorV3,
)


evaluator = DebugCodeEvaluatorV3()


good_code = """
def normalize_scores(
    scores: list[float],
) -> list[float]:
    if not scores:
        return []

    minimum = min(scores)
    maximum = max(scores)

    if minimum == maximum:
        return [0.0 for _ in scores]

    scale = maximum - minimum

    return [
        (score - minimum) / scale
        for score in scores
    ]
""".strip()


buggy_code = """
def normalize_scores(
    scores: list[float],
) -> list[float]:
    scores.sort()

    maximum = max(scores)

    return [
        score / maximum
        for score in scores
    ]
""".strip()


good_result = evaluator.evaluate(
    good_code
)

buggy_result = evaluator.evaluate(
    buggy_code
)


print("Correct repair:")
print("Score:", good_result.score)
print("Passed:", good_result.passed_checks)
print("Failed:", good_result.failed_checks)

print()

print("Buggy implementation:")
print("Score:", buggy_result.score)
print("Passed:", buggy_result.passed_checks)
print("Failed:", buggy_result.failed_checks)


assert good_result.score == 100.0
assert "behavior" in good_result.passed_checks

assert buggy_result.score == 30.0
assert "behavior" in buggy_result.failed_checks


print("\nDebug Code Evaluator V3 test passed.")