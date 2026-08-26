"""
Model benchmarking for AI-OS.

Runs representative AI-OS prompts against a local Ollama model and
records latency and output size. Later versions will support multiple
models and quality scoring.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass
from time import perf_counter
from typing import List
from brain.benchmarks.quality import QualityEvaluator

from brain.models.ollama import OllamaClient


@dataclass
class BenchmarkCase:
    name: str
    prompt: str


@dataclass
class BenchmarkResult:
    model: str
    case_name: str
    duration_seconds: float
    output_characters: int
    quality_score: float
    passed_checks: List[str]
    failed_checks: List[str]
    response: str


class ModelBenchmark:
    def __init__(self, model: str):
        self.model = model
        self.ollama = OllamaClient()
        self.quality = QualityEvaluator()

    def cases(self) -> List[BenchmarkCase]:
        return [
            BenchmarkCase(
                name="planning",
                prompt=(
                    "You are planning development of a local AI operating "
                    "system. Identify the three highest-priority next steps "
                    "and briefly explain why."
                ),
            ),
            BenchmarkCase(
                name="coding",
                prompt=(
                    "Write a small production-quality Python function that "
                    "removes duplicate strings while preserving their "
                    "original order. Include type hints."
                ),
            ),
            BenchmarkCase(
                name="research",
                prompt=(
                    "Compare vector search and keyword search for an AI "
                    "knowledge system. Give strengths, weaknesses, and when "
                    "a hybrid approach is useful."
                ),
            ),
            BenchmarkCase(
                name="reasoning",
                prompt=(
                    "An AI pipeline takes 0.6 seconds for retrieval and "
                    "80 seconds for model generation. Which component should "
                    "be optimized first, and why?"
                ),
            ),
        ]

    def run_case(self, case: BenchmarkCase) -> BenchmarkResult:
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

        return BenchmarkResult(
            model=self.model,
            case_name=case.name,
            duration_seconds=round(duration, 3),
            output_characters=len(response),
            quality_score=quality.score,
            passed_checks=quality.passed_checks,
            failed_checks=quality.failed_checks,
            response=response,
        )

    def save_results(
        self,
        results: List[BenchmarkResult],
        output_directory: Path = Path(
            "brain/benchmarks/results"
        ),
    ) -> Path:
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
            sum(result.duration_seconds for result in results),
            3,
        )

        average_quality = round(
            sum(result.quality_score for result in results)
            / len(results),
            1,
        )

        total_output_characters = sum(
            result.output_characters for result in results
        )

        payload = {
            "model": self.model,
            "created_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "summary": {
                "case_count": len(results),
                "total_duration_seconds": total_duration,
                "average_quality_score": average_quality,
                "total_output_characters": total_output_characters,
            },
            "results": [
                {
                    "case_name": result.case_name,
                    "duration_seconds": result.duration_seconds,
                    "output_characters": result.output_characters,
                    "quality_score": result.quality_score,
                    "passed_checks": result.passed_checks,
                    "failed_checks": result.failed_checks,
                    "response": result.response,
                }
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


    def run(self) -> List[BenchmarkResult]:
        return [
            self.run_case(case)
            for case in self.cases()
        ]