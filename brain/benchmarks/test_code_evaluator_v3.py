from brain.benchmarks.code_evaluator_v3 import (
    CodeEvaluatorV3,
)


evaluator = CodeEvaluatorV3()


good_code = """
def remove_duplicates(
    items: list[str],
) -> list[str]:
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
""".strip()


bad_behavior_code = """
def remove_duplicates(
    items: list[str],
) -> list[str]:
    return list(set(items))
""".strip()


invalid_code = """
def remove_duplicates(
""".strip()


good_result = evaluator.evaluate(
    good_code
)

bad_result = evaluator.evaluate(
    bad_behavior_code
)

invalid_result = evaluator.evaluate(
    invalid_code
)


print("Good code:")
print("Score:", good_result.score)
print("Passed:", good_result.passed_checks)
print("Failed:", good_result.failed_checks)

print()

print("Bad behavior:")
print("Score:", bad_result.score)
print("Passed:", bad_result.passed_checks)
print("Failed:", bad_result.failed_checks)

print()

print("Invalid code:")
print("Score:", invalid_result.score)
print("Passed:", invalid_result.passed_checks)
print("Failed:", invalid_result.failed_checks)


assert good_result.score == 100.0
assert "behavior" in good_result.passed_checks

assert bad_result.score == 30.0
assert "behavior" in bad_result.failed_checks

assert invalid_result.score == 0.0
assert "valid_python" in invalid_result.failed_checks


print("\nCode Evaluator V3 test passed.")