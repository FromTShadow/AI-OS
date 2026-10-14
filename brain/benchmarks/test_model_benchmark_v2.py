from brain.benchmarks.model_benchmark_v2 import BenchmarkCasesV2


def test_benchmark_v2_contains_twelve_cases():
    cases = BenchmarkCasesV2().cases()

    assert len(cases) == 12


def test_benchmark_v2_covers_expected_categories():
    cases = BenchmarkCasesV2().cases()

    assert {case.category for case in cases} == {
        "planning",
        "coding",
        "research",
        "reasoning",
    }


def test_benchmark_v2_has_three_cases_per_category():
    cases = BenchmarkCasesV2().cases()

    for category in {"planning", "coding", "research", "reasoning"}:
        assert sum(case.category == category for case in cases) == 3