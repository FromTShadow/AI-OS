from brain.benchmarks.quality import QualityEvaluator


evaluator = QualityEvaluator()


planning_response = """
The highest priority next steps are:

1. Improve retrieval quality because it supports later features.
2. Add pipeline tests before introducing more complexity.
3. Prepare the planner architecture after the foundation is stable.
"""

coding_response = """
def remove_duplicates(items: list[str]) -> list[str]:
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result

This preserves the original order while removing duplicates.
"""

research_response = """
Vector search is strong at semantic similarity but can have limitations
when exact terminology matters.

Keyword search is strong at exact matching but weaker at semantic meaning.

A hybrid approach combines both methods and can reduce their weaknesses.
"""

reasoning_response = """
Model generation is the bottleneck because it takes 80 seconds while
retrieval takes only 0.6 seconds.

The model generation stage should therefore be optimized first.
"""


tests = {
    "planning": planning_response,
    "coding": coding_response,
    "research": research_response,
    "reasoning": reasoning_response,
}


for case_name, response in tests.items():
    result = evaluator.evaluate(
        case_name=case_name,
        response=response,
    )

    print()
    print("Case:", result.case_name)
    print("Score:", result.score)
    print("Passed:", result.passed_checks)
    print("Failed:", result.failed_checks)

    assert result.score == 100.0


print("\nQuality Evaluator test passed.")