"""
Structured quality evaluation for AI-OS Benchmark V3.

V3 validates actual output structure and task requirements rather
than mainly searching for words in free-form prose.
"""

import json

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class QualityResultV3:
    case_name: str
    score: float
    passed_checks: List[str] = field(default_factory=list)
    failed_checks: List[str] = field(default_factory=list)
    parsed_response: Dict[str, Any] | None = None


class QualityEvaluatorV3:
    def parse_json(
        self,
        response: str,
    ) -> Dict[str, Any] | None:
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed

    def evaluate(
        self,
        case_name: str,
        response: str,
    ) -> QualityResultV3:
        parsed = self.parse_json(response)

        if parsed is None:
            return QualityResultV3(
                case_name=case_name,
                score=0.0,
                failed_checks=["valid_json"],
            )

        if case_name == "planning_priorities_structured":
            return self.evaluate_planning(
                case_name,
                parsed,
            )

        if case_name == "reasoning_bottleneck_structured":
            return self.evaluate_reasoning(
                case_name,
                parsed,
            )

        raise ValueError(
            f"No V3 evaluator configured for case: {case_name}"
        )

    def evaluate_planning(
        self,
        case_name: str,
        parsed: Dict[str, Any],
    ) -> QualityResultV3:
        passed = ["valid_json"]
        failed = []

        priorities = parsed.get("priorities")

        if (
            isinstance(priorities, list)
            and len(priorities) == 3
        ):
            passed.append("exactly_three_priorities")
        else:
            failed.append("exactly_three_priorities")
            priorities = []

        expected_ranks = [1, 2, 3]

        actual_ranks = [
            priority.get("rank")
            for priority in priorities
            if isinstance(priority, dict)
        ]

        if actual_ranks == expected_ranks:
            passed.append("correct_ranks")
        else:
            failed.append("correct_ranks")

        required_fields = {
            "rank",
            "name",
            "rationale",
            "dependencies",
            "tradeoffs",
        }

        complete = (
            len(priorities) == 3
            and all(
                isinstance(priority, dict)
                and required_fields.issubset(priority)
                for priority in priorities
            )
        )

        if complete:
            passed.append("required_fields")
        else:
            failed.append("required_fields")

        nonempty_rationale = (
            len(priorities) == 3
            and all(
                isinstance(priority.get("rationale"), str)
                and priority["rationale"].strip()
                for priority in priorities
                if isinstance(priority, dict)
            )
        )

        if nonempty_rationale:
            passed.append("nonempty_rationale")
        else:
            failed.append("nonempty_rationale")

        structured_lists = (
            len(priorities) == 3
            and all(
                isinstance(priority.get("dependencies"), list)
                and isinstance(priority.get("tradeoffs"), list)
                for priority in priorities
                if isinstance(priority, dict)
            )
        )

        if structured_lists:
            passed.append("structured_dependencies_tradeoffs")
        else:
            failed.append("structured_dependencies_tradeoffs")

        total = len(passed) + len(failed)
        score = len(passed) / total * 100

        return QualityResultV3(
            case_name=case_name,
            score=round(score, 1),
            passed_checks=passed,
            failed_checks=failed,
            parsed_response=parsed,
        )

    def evaluate_reasoning(
        self,
        case_name: str,
        parsed: Dict[str, Any],
    ) -> QualityResultV3:
        passed = ["valid_json"]
        failed = []

        bottleneck = str(
            parsed.get("bottleneck", "")
        ).lower()

        optimize_first = str(
            parsed.get("optimize_first", "")
        ).lower()

        bottleneck_seconds = parsed.get(
            "bottleneck_seconds"
        )

        if "generation" in bottleneck:
            passed.append("correct_bottleneck")
        else:
            failed.append("correct_bottleneck")

        if "generation" in optimize_first:
            passed.append("correct_optimization_target")
        else:
            failed.append("correct_optimization_target")

        if bottleneck_seconds == 75.0:
            passed.append("correct_bottleneck_time")
        else:
            failed.append("correct_bottleneck_time")

        reason = parsed.get("reason")

        if isinstance(reason, str) and reason.strip():
            passed.append("nonempty_reason")
        else:
            failed.append("nonempty_reason")

        total = len(passed) + len(failed)
        score = len(passed) / total * 100

        return QualityResultV3(
            case_name=case_name,
            score=round(score, 1),
            passed_checks=passed,
            failed_checks=failed,
            parsed_response=parsed,
        )