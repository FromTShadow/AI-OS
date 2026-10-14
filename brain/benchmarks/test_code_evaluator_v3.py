import pytest

from brain.benchmarks.code_evaluator_v3 import CodeEvaluatorV3


@pytest.fixture
def evaluator():
    return CodeEvaluatorV3()


def test_evaluator_accepts_correct_implementation(evaluator):
    code = """
def remove_duplicates(items: list[str]) -> list[str]:
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
"""

    result = evaluator.evaluate(code)

    assert result.score == 100.0
    assert "behavior" in result.passed_checks
    assert not result.failed_checks


def test_evaluator_rejects_unordered_implementation(evaluator):
    code = """
def remove_duplicates(items: list[str]) -> list[str]:
    return list(set(items))
"""

    result = evaluator.evaluate(code)

    assert result.score == 30.0
    assert "behavior" in result.failed_checks


def test_evaluator_rejects_invalid_python(evaluator):
    result = evaluator.evaluate("def remove_duplicates(")

    assert result.score == 0.0
    assert "valid_python" in result.failed_checks
    assert result.error