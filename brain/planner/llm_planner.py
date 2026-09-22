"""
Structured LLM Planner for AI-OS.

Uses an LLM to classify tasks and produce a concise execution plan.
Falls back to the deterministic Planner when generation or validation fails.
"""

import json
from typing import Any, Dict, Optional

from brain.models.ollama import OllamaClient
from brain.planner.planner import Planner
from brain.router.router import SUPPORTED_ROLES


REQUIRED_NEEDS = {
    "memory",
    "developer",
    "research",
    "second_brain",
    "trading",
    "ceo",
}


class PlanValidationError(ValueError):
    """Raised when an LLM-generated plan does not match the required schema."""


class LLMPlanner:
    def __init__(
        self,
        ollama: Optional[OllamaClient] = None,
        fallback: Optional[Planner] = None,
        model: Optional[str] = None,
        max_attempts: int = 2,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")

        self.ollama = ollama or OllamaClient()
        self.fallback = fallback or Planner()
        self.model = model
        self.max_attempts = max_attempts

    def build_prompt(self, query: str) -> str:
        roles = ", ".join(sorted(SUPPORTED_ROLES))

        return f"""
You are the planning component of AI-OS.

Analyze the user request and return ONLY valid JSON.
Do not include Markdown fences or additional text.

Supported specialist roles:
{roles}

Required JSON structure:
{{
  "query": "original user request",
  "needs": {{
    "memory": true,
    "developer": false,
    "research": false,
    "second_brain": false,
    "trading": false,
    "ceo": false
  }},
  "primary_role": "one supported role",
  "goal": "short description of the requested outcome",
  "steps": [
    "concrete execution step"
  ],
  "risks": [
    "important risk or limitation"
  ],
  "success_criteria": [
    "observable completion condition"
  ]
}}

Rules:
- Enable developer for requests involving code, Python, APIs, debugging, implementation, or building technical systems.
- Do not invent specific models, frameworks, libraries, or infrastructure that the user did not provide.
- Preserve the original user request in "query".
- Every key under "needs" must be present and boolean.
- Set memory to true when prior knowledge or project context could help.
- Select all relevant specialist roles under "needs".
- primary_role must be one supported specialist role.
- primary_role must also be enabled under "needs".
- Provide between 1 and 5 concise steps.
- Provide between 0 and 3 risks.
- Provide between 1 and 3 success criteria.
- Do not claim that any work has already been completed.

User request:
{query}
""".strip()

    def extract_json(self, response: str) -> Dict[str, Any]:
        text = response.strip()

        if text.startswith("```"):
            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            raise PlanValidationError(
                f"Planner response is not valid JSON: {error}"
            ) from error

        if not isinstance(data, dict):
            raise PlanValidationError(
                "Planner response must be a JSON object."
            )

        return data

    def validate(
        self,
        plan: Dict[str, Any],
        query: str,
    ) -> Dict[str, Any]:
        needs = plan.get("needs")

        if not isinstance(needs, dict):
            raise PlanValidationError(
                "'needs' must be an object."
            )

        if set(needs) != REQUIRED_NEEDS:
            raise PlanValidationError(
                "'needs' must contain exactly the required keys."
            )

        if not all(
            isinstance(value, bool)
            for value in needs.values()
        ):
            raise PlanValidationError(
                "Every value under 'needs' must be boolean."
            )

        primary_role = plan.get("primary_role")

        if primary_role not in SUPPORTED_ROLES:
            raise PlanValidationError(
                f"Unsupported primary role: {primary_role!r}"
            )

        if not needs[primary_role]:
            raise PlanValidationError(
                "The primary role must be enabled under 'needs'."
            )

        goal = plan.get("goal")

        if not isinstance(goal, str) or not goal.strip():
            raise PlanValidationError(
                "'goal' must be a non-empty string."
            )

        steps = plan.get("steps")
        self.validate_string_list(
            name="steps",
            value=steps,
            minimum=1,
            maximum=5,
        )

        risks = plan.get("risks")
        self.validate_string_list(
            name="risks",
            value=risks,
            minimum=0,
            maximum=3,
        )

        success_criteria = plan.get("success_criteria")
        self.validate_string_list(
            name="success_criteria",
            value=success_criteria,
            minimum=1,
            maximum=3,
        )

        return {
            "query": query,
            "needs": needs,
            "primary_role": primary_role,
            "goal": goal.strip(),
            "steps": steps,
            "risks": risks,
            "success_criteria": success_criteria,
            "planner_type": "llm",
            "fallback_reason": None,
        }

    def validate_string_list(
        self,
        name: str,
        value: Any,
        minimum: int,
        maximum: int,
    ) -> None:
        if not isinstance(value, list):
            raise PlanValidationError(
                f"'{name}' must be a list."
            )

        if not minimum <= len(value) <= maximum:
            raise PlanValidationError(
                f"'{name}' must contain between "
                f"{minimum} and {maximum} items."
            )

        if not all(
            isinstance(item, str) and item.strip()
            for item in value
        ):
            raise PlanValidationError(
                f"Every item in '{name}' must be a non-empty string."
            )

    def fallback_plan(
        self,
        query: str,
        reason: str,
        attempts: int,
    ) -> Dict[str, Any]:
        plan = self.fallback.classify(query)
        plan["goal"] = query
        plan["steps"] = []
        plan["risks"] = []
        plan["success_criteria"] = []
        plan["planner_type"] = "deterministic_fallback"
        plan["planner_attempts"] = attempts
        plan["fallback_reason"] = reason
        return plan

    def apply_deterministic_guardrails(
        self,
        plan: Dict[str, Any],
        query: str,
    ) -> Dict[str, Any]:
        baseline = self.fallback.classify(query)
        baseline_needs = baseline["needs"]

        for role, needed in baseline_needs.items():
            if needed:
                plan["needs"][role] = True

        plan["guardrail_roles"] = [
            role
            for role, needed in baseline_needs.items()
            if role != "memory" and needed
        ]

        return plan

    def classify(self, query: str) -> Dict[str, Any]:
        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("Query cannot be empty.")

        errors = []

        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self.ollama.chat(
                    self.build_prompt(cleaned_query),
                    model=self.model,
                    temperature=0.0,
                    seed=42,
                    max_tokens=700,
                    timeout=180,
                )
                raw_plan = self.extract_json(response)
                plan = self.validate(
                    raw_plan,
                    cleaned_query,
                )
                plan = self.apply_deterministic_guardrails(
                    plan,
                    cleaned_query,
                )
                plan["planner_attempts"] = attempt
                return plan
            except Exception as error:
                errors.append(
                    f"attempt {attempt}: "
                    f"{type(error).__name__}: {error}"
                )

        return self.fallback_plan(
            cleaned_query,
            reason=" | ".join(errors),
            attempts=self.max_attempts,
        )