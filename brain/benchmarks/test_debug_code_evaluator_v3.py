import pytest

from brain.benchmarks.debug_code_evaluator_v3 import (
    DebugCodeEvaluatorV3,
)


@pytest.fixture
def evaluator():
    return DebugCodeEvaluatorV3()


def test_debug_evaluator_accepts_correct_implementation(evaluator):
    code = """
def normalize_scores(scores: list[float]) -> list[float]:
    if not scores:
        return []

    minimum = min(scores)
    maximum = max(scores)

    if minimum == maximum:
        return [0.0 for _ in scores]

    scale = maximum - minimum

    return [(score - minimum) / scale for score in scores]
"""

    result = evaluator.evaluate(code)

    assert result.score == 100.0
    assert "behavior" in result.passed_checks
    assert not result.failed_checks


def test_debug_evaluator_rejects_buggy_implementation(evaluator):
    code = """
def normalize_scores(scores: list[float]) -> list[float]:
    scores.sort()
    maximum = max(scores)

    return [score / maximum for score in scores]
"""

    result = evaluator.evaluate(code)

    assert result.score == 30.0
    assert "behavior" in result.failed_checks