"""
Command-line runner for AI-OS Model Benchmark V3.

Usage:
    python -m brain.benchmarks.run_v3 <model>
"""

import sys

from brain.benchmarks.runner_v3 import ModelBenchmarkRunnerV3


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python -m brain.benchmarks.run_v3 <model>"
        )

    model = sys.argv[1]

    runner = ModelBenchmarkRunnerV3(
        model=model,
    )

    print("=" * 60)
    print("AI-OS MODEL BENCHMARK V3")
    print("=" * 60)
    print("Model:", model)
    print()

    results = runner.run()

    for result in results:
        print(
            f"{result.category:10} | "
            f"{result.case_name:32} | "
            f"{result.duration_seconds:8.3f}s | "
            f"quality={result.quality_score:5.1f}%"
        )

        if result.failed_checks:
            print(
                " " * 13,
                "Failed:",
                result.failed_checks,
            )

    print()

    total_duration = sum(
        result.duration_seconds
        for result in results
    )

    average_quality = (
        sum(result.quality_score for result in results)
        / len(results)
    )

    print("Total duration:", round(total_duration, 3), "seconds")
    print("Average quality:", round(average_quality, 1), "%")


if __name__ == "__main__":
    main()