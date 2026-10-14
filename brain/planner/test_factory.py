from brain.planner.factory import create_planner
from brain.planner.llm_planner import LLMPlanner
from brain.planner.planner import Planner


def test_create_deterministic_planner():
    planner = create_planner(mode="deterministic")

    assert isinstance(planner, Planner)


def test_create_llm_planner_with_custom_settings():
    planner = create_planner(
        mode="llm",
        model="test-model",
        max_attempts=3,
    )

    assert isinstance(planner, LLMPlanner)
    assert planner.model == "test-model"
    assert planner.max_attempts == 3


def test_unknown_planner_mode_is_rejected():
    try:
        create_planner(mode="unknown")
    except ValueError as error:
        assert "Unsupported planner mode" in str(error)
    else:
        raise AssertionError(
            "Unknown planner mode should raise ValueError."
        )


def test_default_planner_uses_configured_settings():
    planner = create_planner()

    assert isinstance(planner, LLMPlanner)
    assert planner.model == "qwen3.5:4b"
    assert planner.max_attempts == 2