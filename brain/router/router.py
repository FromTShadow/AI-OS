"""
Specialist Router for AI-OS.

Converts a Planner result into a validated specialist prompt bundle.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from brain.router.loader import PromptDocument, PromptLoader


SUPPORTED_ROLES = {
    "developer",
    "research",
    "second_brain",
    "trading",
    "ceo",
}


@dataclass(frozen=True)
class RouteDecision:
    primary_role: str
    specialists: List[str]
    system_prompt: PromptDocument
    primary_prompt: PromptDocument


class SpecialistRouter:
    def __init__(self, loader: Optional[PromptLoader] = None):
        self.loader = loader or PromptLoader()

    def normalize_role(self, role: str) -> str:
        normalized = role.strip().lower().replace("-", "_")

        if normalized not in SUPPORTED_ROLES:
            return "ceo"

        return normalized

    def active_specialists(self, plan: Dict) -> List[str]:
        needs = plan.get("needs", {})

        specialists = [
            role
            for role, needed in needs.items()
            if role != "memory"
            and needed
            and role in SUPPORTED_ROLES
        ]

        primary_role = self.normalize_role(
            plan.get("primary_role", "ceo")
        )

        if primary_role not in specialists:
            specialists.insert(0, primary_role)

        return specialists

    def route(self, plan: Dict) -> RouteDecision:
        primary_role = self.normalize_role(
            plan.get("primary_role", "ceo")
        )

        specialists = self.active_specialists(plan)
        bundle = self.loader.load_bundle(primary_role)

        return RouteDecision(
            primary_role=primary_role,
            specialists=specialists,
            system_prompt=bundle["system"],
            primary_prompt=bundle["specialist"],
        )