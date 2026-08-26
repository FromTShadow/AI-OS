"""
Execution runner for AI-OS Model Benchmark V2.

Runs the 12-case benchmark against an Ollama model,
scores responses with QualityEvaluatorV2, and persists
the results as JSON.
"""

import json

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import List

from brain.benchmarks.model_benchmark_v2 import (
    BenchmarkCaseV2,
    BenchmarkCasesV2,
)
from brain.benchmarks.quality_v2 import QualityEvaluatorV2
from brain.models.ollama import OllamaClient


@dataclass
class BenchmarkResultV2:
    model: str
    case_name: str
    category: str
    duration_seconds: float
    output_characters: int
    quality_score: float
    passed_checks: List[str]
    failed_checks: List[str]
    response: str


class ModelBenchmarkRunnerV2:
    def __init__(self, model: str):
        self.model = model
        self.ollama = OllamaClient()
        self.case_provider = BenchmarkCasesV2()
        self.quality = QualityEvaluatorV2()

    def run_case(
        self,
        case: BenchmarkCaseV2,
    ) -> BenchmarkResultV2:
        started_at = perf_counter()

        response = self.ollama.chat(
            case.prompt,
            model=self.model,
        )

        duration = perf_counter() - started_at

        quality = self.quality.evaluate(
            case_name=case.name,
            response=response,
        )

        return BenchmarkResultV2(
            model=self.model,
            case_name=case.name,
            category=case.category,
            duration_seconds=round(duration, 3),
            output_characters=len(response),
            quality_score=quality.score,
            passed_checks=quality.passed_checks,
            failed_checks=quality.failed_checks,
            response=response,
        )

    def run(self) -> List[BenchmarkResultV2]:
        return [
            self.run_case(case)
            for case in self.case_provider.cases()
        ]

    def save_results(
        self,
        results: List[BenchmarkResultV2],
        output_directory: Path = Path(
            "brain/benchmarks/results_v2"
        ),
    ) -> Path:
        if not results:
            raise ValueError(
                "Cannot save an empty benchmark result set."
            )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_model_name = (
            self.model
            .replace(":", "-")
            .replace("/", "-")
        )

        output_path = (
            output_directory
            / f"{safe_model_name}.json"
        )

        total_duration = round(
            sum(
                result.duration_seconds
                for result in results
            ),
            3,
        )

        average_quality = round(
            sum(
                result.quality_score
                for result in results
            )
            / len(results),
            1,
        )

        category_summary = {}

        for category in sorted(
            {result.category for result in results}
        ):
            category_results = [
                result
                for result in results
                if result.category == category
            ]

            category_summary[category] = {
                "case_count": len(category_results),
                "total_duration_seconds": round(
                    sum(
                        result.duration_seconds
                        for result in category_results
                    ),
                    3,
                ),
                "average_quality_score": round(
                    sum(
                        result.quality_score
                        for result in category_results
                    )
                    / len(category_results),
                    1,
                ),
            }

        payload = {
            "benchmark_version": 2,
            "model": self.model,
            "created_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "summary": {
                "case_count": len(results),
                "total_duration_seconds": total_duration,
                "average_quality_score": average_quality,
                "categories": category_summary,
            },
            "results": [
                asdict(result)
                for result in results
            ],
        }

        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output_path