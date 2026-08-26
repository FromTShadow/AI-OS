"""
Stronger deterministic quality evaluation for AI-OS benchmarks.

Version 2 supports:
- any-of requirements
- all-of requirements
- weighted checks

The evaluator remains deterministic and explainable.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class QualityCheck:
    name: str
    weight: float = 1.0
    any_of: List[str] = field(default_factory=list)
    all_of: List[str] = field(default_factory=list)


@dataclass
class QualityResult:
    case_name: str
    score: float
    passed_checks: List[str]
    failed_checks: List[str]


class QualityEvaluatorV2:
    def __init__(self):


        self.case_specific_checks = {
            "planning_priorities": [
                QualityCheck(
                    name="mentions_llm_planner",
                    weight=2.0,
                    any_of=[
                        "llm planner",
                        "planner",
                    ],
                ),
                QualityCheck(
                    name="mentions_multi_agent",
                    any_of=[
                        "multi-agent",
                        "multi agent",
                    ],
                ),
            ],
            "coding_debugging": [
                QualityCheck(
                    name="identifies_set_order_issue",
                    weight=2.0,
                    all_of=[
                        "set",
                        "order",
                    ],
                ),
            ],
            "coding_architecture": [
                QualityCheck(
                    name="shared_context_object",
                    weight=2.0,
                    any_of=[
                        "task",
                        "executioncontext",
                        "execution context",
                    ],
                ),
            ],
            "research_uncertainty": [
                QualityCheck(
                    name="limited_evidence",
                    weight=2.0,
                    any_of=[
                        "limited",
                        "more runs",
                        "more tests",
                        "repeat",
                        "variance",
                    ],
                ),
            ],
            "reasoning_constraints": [
                QualityCheck(
                    name="memory_headroom",
                    weight=2.0,
                    any_of=[
                        "headroom",
                        "memory",
                        "ram",
                    ],
                ),
                QualityCheck(
                    name="smaller_default",
                    any_of=[
                        "model a",
                        "smaller model",
                        "6 gb",
                    ],
                ),
            ],
            "reasoning_tradeoff": [
                QualityCheck(
                    name="role_specific_choice",
                    weight=2.0,
                    all_of=[
                        "planning",
                        "coding",
                        "research",
                    ],
                ),
            ],
        }
        self.case_checks: Dict[str, List[QualityCheck]] = {
            "planning": [
                QualityCheck(
                    name="priorities",
                    weight=2.0,
                    any_of=[
                        "priority",
                        "priorities",
                        "next step",
                        "next steps",
                    ],
                ),
                QualityCheck(
                    name="rationale",
                    any_of=[
                        "because",
                        "why",
                        "reason",
                    ],
                ),
                QualityCheck(
                    name="dependencies",
                    any_of=[
                        "dependency",
                        "foundation",
                        "before",
                    ],
                ),
            ],

            "coding": [
                QualityCheck(
                    name="function",
                    weight=2.0,
                    any_of=["def "],
                ),
                QualityCheck(
                    name="return_type",
                    any_of=["->"],
                ),
                QualityCheck(
                    name="duplicate_logic",
                    weight=2.0,
                    any_of=[
                        "seen",
                        "set(",
                        "dict",
                    ],
                ),
                QualityCheck(
                    name="order_preservation",
                    any_of=[
                        "preserve",
                        "preserving",
                        "original order",
                    ],
                ),
            ],

            "research": [
                QualityCheck(
                    name="both_search_types",
                    weight=2.0,
                    all_of=[
                        "vector search",
                        "keyword search",
                    ],
                ),
                QualityCheck(
                    name="strengths",
                    any_of=[
                        "strength",
                        "strong",
                        "advantage",
                    ],
                ),
                QualityCheck(
                    name="weaknesses",
                    any_of=[
                        "weakness",
                        "limitation",
                        "disadvantage",
                    ],
                ),
                QualityCheck(
                    name="hybrid",
                    weight=2.0,
                    any_of=[
                        "hybrid",
                        "combine",
                        "combined",
                    ],
                ),
            ],

            "reasoning": [
                QualityCheck(
                    name="identify_bottleneck",
                    weight=2.0,
                    any_of=["bottleneck"],
                ),
                QualityCheck(
                    name="generation_stage",
                    all_of=[
                        "model",
                        "generation",
                    ],
                ),
                QualityCheck(
                    name="uses_both_timings",
                    weight=2.0,
                    all_of=[
                        "80",
                        "0.6",
                    ],
                ),
                QualityCheck(
                    name="correct_optimization_target",
                    weight=2.0,
                    all_of=[
                        "optimiz",
                        "generation",
                    ],
                ),
            ],
        }

        self.case_categories = {
            "planning_priorities": "planning",
            "planning_conflict": "planning",
            "planning_architecture": "planning",
            "coding_implementation": "coding",
            "coding_debugging": "coding",
            "coding_architecture": "coding",
            "research_comparison": "research",
            "research_synthesis": "research",
            "research_uncertainty": "research",
            "reasoning_bottleneck": "reasoning",
            "reasoning_constraints": "reasoning",
            "reasoning_tradeoff": "reasoning",
        }

        self.case_categories = {
            "planning_priorities": "planning",
            "planning_conflict": "planning",
            "planning_architecture": "planning",
            "coding_implementation": "coding",
            "coding_debugging": "coding",
            "coding_architecture": "coding",
            "research_comparison": "research",
            "research_synthesis": "research",
            "research_uncertainty": "research",
            "reasoning_bottleneck": "reasoning",
            "reasoning_constraints": "reasoning",
            "reasoning_tradeoff": "reasoning",
        }

    def check_passes(
        self,
        check: QualityCheck,
        text: str,
    ) -> bool:
        if check.any_of:
            if not any(
                phrase.lower() in text
                for phrase in check.any_of
            ):
                return False

        if check.all_of:
            if not all(
                phrase.lower() in text
                for phrase in check.all_of
            ):
                return False

        return True

    def evaluate(
        self,
        case_name: str,
        response: str,
    ) -> QualityResult:
        resolved_case = self.case_categories.get(
            case_name,
            case_name,
        )

        checks = self.case_checks.get(resolved_case)

        checks = list(checks)

        checks.extend(
            self.case_specific_checks.get(
                case_name,
                [],
            )
        )

        if checks is None:
            raise ValueError(
                f"No quality checks configured for case: {case_name}"
            )

        text = response.lower()

        passed = []
        failed = []

        earned_weight = 0.0
        total_weight = sum(
            check.weight
            for check in checks
        )

        for check in checks:
            if self.check_passes(check, text):
                passed.append(check.name)
                earned_weight += check.weight
            else:
                failed.append(check.name)

        score = (
            earned_weight / total_weight * 100
            if total_weight
            else 0.0
        )

        return QualityResult(
            case_name=case_name,
            score=round(score, 1),
            passed_checks=passed,
            failed_checks=failed,
        )