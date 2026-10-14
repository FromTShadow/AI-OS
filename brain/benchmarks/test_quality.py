import pytest

from brain.benchmarks.quality import QualityEvaluator


@pytest.fixture
def evaluator():
    return QualityEvaluator()


@pytest.mark.parametrize(
    ("case_name", "response"),
    [
        (
            "planning",
            """
            The highest priorities and next steps are:

            1. Improve retrieval quality because it supports later features.
            2. Add pipeline tests before introducing more complexity.
            3. Prepare the planner architecture after the foundation is stable.
            """,
        ),
        (
            "coding",
            """
            def remove_duplicates(items: list[str]) -> list[str]:
                seen = set()
                result = []
                for item in items:
                    if item not in seen:
                        seen.add(item)
                        result.append(item)
                return result

            This preserves the original order while removing duplicates.
            """,
        ),
        (
            "research",
            """
            Vector search is strong at semantic similarity but can have
            limitations when exact terminology matters.
            Keyword search is strong at exact matching but weaker at
            semantic meaning.
            A hybrid approach combines both methods.
            """,
        ),
        (
            "reasoning",
            """
            Model generation is the bottleneck because it takes 80 seconds
            while retrieval takes only 0.6 seconds.
            Model generation should therefore be optimized first.
            """,
        ),
    ],
)
def test_quality_evaluator_accepts_good_responses(
    evaluator, case_name, response
):
    result = evaluator.evaluate(case_name=case_name, response=response)

    assert result.score == 100.0