"""
Execution runner for AI-OS Model Benchmark V3.
"""

from dataclasses import dataclass
from time import perf_counter
from typing import List
from urllib import response
from brain.benchmarks.code_evaluator_v3 import CodeEvaluatorV3

from brain.benchmarks.model_benchmark_v3 import (
    BenchmarkCaseV3,
    BenchmarkCasesV3,
)
from brain.benchmarks.quality_v3 import QualityEvaluatorV3
from brain.models.ollama import OllamaClient
from brain.benchmarks.debug_code_evaluator_v3 import (
    DebugCodeEvaluatorV3,
)


@dataclass
class BenchmarkResultV3:
    model: str
    case_name: str
    category: str
    duration_seconds: float
    quality_score: float
    passed_checks: List[str]
    failed_checks: List[str]
    response: str


class ModelBenchmarkRunnerV3:
    def __init__(self, model: str):
        self.model = model
        self.ollama = OllamaClient()
        self.case_provider = BenchmarkCasesV3()
        self.quality = QualityEvaluatorV3()
        self.code_quality = CodeEvaluatorV3()
        self.debug_code_quality = DebugCodeEvaluatorV3()

    def run_case(
        self,
        case: BenchmarkCaseV3,
    ) -> BenchmarkResultV3:
        started_at = perf_counter()

        response = self.ollama.chat(
            case.prompt,
            model=self.model,
            temperature=0.0,
            seed=42,
        )

        duration = perf_counter() - started_at

        if case.name == "coding_normalize_scores_debug":
            quality = self.debug_code_quality.evaluate(
        response
    )
        elif case.category == "coding":
            quality = self.code_quality.evaluate(
        response
    )
        else:
            quality = self.quality.evaluate(
                case_name=case.name,
                response=response,
    )

        return BenchmarkResultV3(
            model=self.model,
            case_name=case.name,
            category=case.category,
            duration_seconds=round(duration, 3),
            quality_score=quality.score,
            passed_checks=quality.passed_checks,
            failed_checks=quality.failed_checks,
            response=response,
        )

    def run(self) -> List[BenchmarkResultV3]:
        return [
            self.run_case(case)
            for case in self.case_provider.cases()
        ]