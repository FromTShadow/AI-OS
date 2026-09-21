"""
Reliability benchmarking for AI-OS Benchmark V3.

Runs the same benchmark case multiple times and records:
- success rate
- cold-start latency
- warm median latency
- average quality
"""

from dataclasses import dataclass
from statistics import median
from typing import List

from brain.benchmarks.model_benchmark_v3 import BenchmarkCaseV3
from brain.benchmarks.runner_v3 import (
    BenchmarkResultV3,
    ModelBenchmarkRunnerV3,
)


@dataclass
class ReliabilityResultV3:
    model: str
    case_name: str
    trials: int
    successful_trials: int
    success_rate: float
    cold_start_seconds: float
    warm_median_seconds: float
    average_quality: float
    results: List[BenchmarkResultV3]


class ReliabilityBenchmarkV3:
    def __init__(
        self,
        model: str,
        trials: int = 3,
    ):
        if trials < 2:
            raise ValueError(
                "trials must be at least 2."
            )

        self.model = model
        self.trials = trials
        self.runner = ModelBenchmarkRunnerV3(
            model=model,
        )

    def run_case(
        self,
        case: BenchmarkCaseV3,
    ) -> ReliabilityResultV3:
        results = [
            self.runner.run_case(case)
            for _ in range(self.trials)
        ]

        successful_trials = sum(
            1
            for result in results
            if result.quality_score == 100.0
        )

        success_rate = (
            successful_trials
            / self.trials
            * 100
        )

        cold_start_seconds = (
            results[0].duration_seconds
        )

        warm_times = [
            result.duration_seconds
            for result in results[1:]
        ]

        warm_median_seconds = median(
            warm_times
        )

        average_quality = (
            sum(
                result.quality_score
                for result in results
            )
            / self.trials
        )

        return ReliabilityResultV3(
            model=self.model,
            case_name=case.name,
            trials=self.trials,
            successful_trials=successful_trials,
            success_rate=round(
                success_rate,
                1,
            ),
            cold_start_seconds=round(
                cold_start_seconds,
                3,
            ),
            warm_median_seconds=round(
                warm_median_seconds,
                3,
            ),
            average_quality=round(
                average_quality,
                1,
            ),
            results=results,
        )