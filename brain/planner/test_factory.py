from brain.planner.factory import create_planner
from brain.planner.llm_planner import LLMPlanner
from brain.planner.planner import Planner


deterministic = create_planner(
    mode="deterministic"
)

assert isinstance(deterministic, Planner)


llm = create_planner(
    mode="llm",
    model="test-model",
    max_attempts=3,
)

assert isinstance(llm, LLMPlanner)
assert llm.model == "test-model"
assert llm.max_attempts == 3


try:
    create_planner(mode="unknown")
except ValueError as error:
    assert "Unsupported planner mode" in str(error)
else:
    raise AssertionError(
        "Unknown planner mode should raise ValueError."
    )

configured_default = create_planner()

assert isinstance(configured_default, LLMPlanner)
assert configured_default.model == "qwen3.5:4b"
assert configured_default.max_attempts == 2


print("Planner factory test passed.")