"""
Planner factory for AI-OS.

Creates the configured planning implementation while keeping planner
selection outside the execution pipeline.
"""

from typing import Optional

from brain.config.settings import (
    LLM_PLANNER_MAX_ATTEMPTS,
    LLM_PLANNER_MODEL,
    PLANNER_MODE,
)
from brain.planner.llm_planner import LLMPlanner
from brain.planner.planner import Planner


SUPPORTED_PLANNER_MODES = {
    "deterministic",
    "llm",
}


def create_planner(
    mode: Optional[str] = None,
    model: Optional[str] = None,
    max_attempts: Optional[int] = None,
):
    selected_mode = (
        mode if mode is not None else PLANNER_MODE
    ).strip().lower()

    if selected_mode not in SUPPORTED_PLANNER_MODES:
        raise ValueError(
            f"Unsupported planner mode: {selected_mode!r}. "
            f"Expected one of: "
            f"{sorted(SUPPORTED_PLANNER_MODES)}"
        )

    if selected_mode == "deterministic":
        return Planner()

    selected_model = (
        model if model is not None else LLM_PLANNER_MODEL
    )
    selected_attempts = (
        max_attempts
        if max_attempts is not None
        else LLM_PLANNER_MAX_ATTEMPTS
    )

    return LLMPlanner(
        model=selected_model,
        max_attempts=selected_attempts,
    )