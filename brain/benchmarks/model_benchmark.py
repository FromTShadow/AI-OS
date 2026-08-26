"""
Model benchmarking for AI-OS.

Runs representative AI-OS prompts against a local Ollama model and
records latency and output size. Later versions will support multiple
models and quality scoring.
"""

from dataclasses import dataclass
from time import perf_counter
from typing import List

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
    response: str


class ModelBenchmark:
    def __init__(self, model: str):
        self.model = model
        self.ollama = OllamaClient()

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
        
        return BenchmarkResult(
            model=self.model,
            case_name=case.name,
            duration_seconds=round(duration, 3),
            output_characters=len(response),
            response=response,
        )

    def run(self) -> List[BenchmarkResult]:
        return [
            self.run_case(case)
            for case in self.cases()
        ]