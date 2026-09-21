"""
Command-line runner for AI-OS Benchmark V3 reliability tests.

Usage:
    python -m brain.benchmarks.run_reliability_v3 \
        <model> <case_name>
"""

import sys

from brain.benchmarks.reliability_v3 import (
    ReliabilityBenchmarkV3,
)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python -m brain.benchmarks.run_reliability_v3 "
            "<model> <case_name>"
        )

    model = sys.argv[1]
    case_name = sys.argv[2]

    benchmark = ReliabilityBenchmarkV3(
        model=model,
        trials=3,
    )

    case = next(
        (
            case
            for case in benchmark.runner.case_provider.cases()
            if case.name == case_name
        ),
        None,
    )

    if case is None:
        raise SystemExit(
            f"Unknown benchmark case: {case_name}"
        )

    print("=" * 60)
    print("AI-OS RELIABILITY BENCHMARK V3")
    print("=" * 60)
    print("Model:", model)
    print("Case:", case_name)
    print("Trials:", benchmark.trials)

    result = benchmark.run_case(case)

    print()
    print("Success rate:", result.success_rate, "%")
    print("Successful trials:", result.successful_trials)
    print("Average quality:", result.average_quality, "%")
    print("Cold-start:", result.cold_start_seconds, "s")
    print("Warm median:", result.warm_median_seconds, "s")

    print()
    print("Individual trials:")

    for index, trial in enumerate(
        result.results,
        start=1,
    ):
        print(
            f"  {index}: "
            f"{trial.duration_seconds}s | "
            f"quality={trial.quality_score}%"
        )


if __name__ == "__main__":
    main()