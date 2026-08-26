"""
Deterministic quality evaluation for AI-OS model benchmarks.

This module performs simple, explainable checks against benchmark
responses. It is intentionally conservative and should be treated as
one signal, not a perfect measure of model intelligence.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class QualityResult:
    case_name: str
    score: float
    passed_checks: List[str]
    failed_checks: List[str]


class QualityEvaluator:
    def __init__(self):
        self.case_checks: Dict[str, Dict[str, List[str]]] = {
            "planning": {
                "priorities": [
                    "priority",
                    "priorities",
                    "next step",
                    "next steps",
                ],
                "rationale": [
                    "because",
                    "why",
                    "reason",
                ],
                "dependencies": [
                    "dependency",
                    "foundation",
                    "before",
                ],
            },
            "coding": {
                "function": [
                    "def ",
                ],
                "type_hints": [
                    "->",
                    ": str",
                    ": list",
                    ": iterable",
                ],
                "duplicate_logic": [
                    "duplicate",
                    "seen",
                    "dict",
                    "set",
                ],
                "order": [
                    "order",
                    "preserv",
                ],
            },
            "research": {
                "vector_search": [
                    "vector search",
                ],
                "keyword_search": [
                    "keyword search",
                ],
                "strengths": [
                    "strength",
                    "strong",
                    "advantage",
                ],
                "weaknesses": [
                    "weakness",
                    "limitation",
                    "disadvantage",
                ],
                "hybrid": [
                    "hybrid",
                    "combine",
                    "combined",
                ],
            },
            "reasoning": {
                "bottleneck": [
                    "bottleneck",
                ],
                "generation": [
                    "generation",
                    "model",
                ],
                "timing": [
                    "80",
                    "0.6",
                ],
                "optimize_model": [
                    "optimize",
                    "generation",
                ],
            },
        }

    def evaluate(
        self,
        case_name: str,
        response: str,
    ) -> QualityResult:
        checks = self.case_checks.get(case_name)

        if checks is None:
            raise ValueError(
                f"No quality checks configured for case: {case_name}"
            )

        text = response.lower()

        passed = []
        failed = []

        for check_name, keywords in checks.items():
            if any(keyword.lower() in text for keyword in keywords):
                passed.append(check_name)
            else:
                failed.append(check_name)

        total_checks = len(checks)

        score = (
            len(passed) / total_checks * 100
            if total_checks
            else 0.0
        )

        return QualityResult(
            case_name=case_name,
            score=round(score, 1),
            passed_checks=passed,
            failed_checks=failed,
        )