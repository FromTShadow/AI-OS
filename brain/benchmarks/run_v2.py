"""
Command-line runner for AI-OS Model Benchmark V2.

Usage:
    python -m brain.benchmarks.run_v2 qwen3.5:4b
"""

import sys

from brain.benchmarks.runner_v2 import ModelBenchmarkRunnerV2


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python -m brain.benchmarks.run_v2 <model>"
        )

    model = sys.argv[1]

    runner = ModelBenchmarkRunnerV2(
        model=model,
    )

    print("=" * 60)
    print("AI-OS MODEL BENCHMARK V2")
    print("=" * 60)
    print("Model:", model)
    print()

    results = runner.run()

    for result in results:
        print(
            f"{result.category:10} | "
            f"{result.case_name:24} | "
            f"{result.duration_seconds:8.3f}s | "
            f"quality={result.quality_score:5.1f}%"
        )

    output_path = runner.save_results(results)

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total_duration = sum(
        result.duration_seconds
        for result in results
    )

    average_quality = (
        sum(
            result.quality_score
            for result in results
        )
        / len(results)
    )

    print(
        "Total duration:",
        round(total_duration, 3),
        "seconds",
    )

    print(
        "Average quality:",
        round(average_quality, 1),
        "%",
    )

    print("Saved:", output_path)


if __name__ == "__main__":
    main()