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


print("Planner factory test passed.")