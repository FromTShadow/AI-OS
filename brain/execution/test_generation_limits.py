"""
Tests role-specific model generation limits without calling Ollama.
"""

from brain.config.settings import PIPELINE_CHAT_TIMEOUT_SECONDS
from brain.execution.pipeline import ExecutionPipeline
from brain.execution.task import Task


class FakeOllama:
    default_model = "fake-model"

    def __init__(self):
        self.calls = []

    def chat(self, prompt: str, **kwargs) -> str:
        self.calls.append({
            "prompt": prompt,
            **kwargs,
        })
        return "Generated response."


def test_model_max_tokens_by_role():
    pipeline = object.__new__(ExecutionPipeline)

    expected_limits = {
        "research": 1400,
        "developer": 1200,
        "trading": 1200,
        "second_brain": 1000,
        "ceo": 900,
        "general": 900,
        "unknown_role": 900,
    }

    for role, expected_limit in expected_limits.items():
        task = Task(query="Test")
        task.primary_role = None if role == "general" else role

        actual_limit = pipeline.model_max_tokens(task)

        assert actual_limit == expected_limit, (
            f"{role}: expected {expected_limit}, got {actual_limit}"
        )


def test_run_model_records_generation_metadata():
    pipeline = object.__new__(ExecutionPipeline)
    pipeline.ollama = FakeOllama()

    task = Task(query="Test model execution")
    task.primary_role = "research"
    task.prompt = "Research prompt"

    result = pipeline.run_model(task)

    assert result.answer == "Generated response."
    assert pipeline.ollama.calls == [
        {
            "prompt": "Research prompt",
            "max_tokens": 1400,
            "timeout": PIPELINE_CHAT_TIMEOUT_SECONDS,
        }
    ]
    assert result.metadata["model_generation"] == {
        "model": "fake-model",
        "max_tokens": 1400,
        "timeout_seconds": PIPELINE_CHAT_TIMEOUT_SECONDS,
    }
