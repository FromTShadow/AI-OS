import json

from brain.planner.llm_planner import LLMPlanner


class FakeOllamaClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def chat(self, prompt, **kwargs):
        self.calls.append(
            {
                "prompt": prompt,
                "kwargs": kwargs,
            }
        )

        if not self.responses:
            raise AssertionError(
                "Fake Ollama received more calls than expected."
            )

        response = self.responses.pop(0)

        if isinstance(response, Exception):
            raise response

        return response


def valid_plan(**overrides):
    plan = {
        "query": "Research local AI models",
        "needs": {
            "memory": True,
            "developer": False,
            "research": True,
            "second_brain": False,
            "trading": False,
            "ceo": False,
        },
        "primary_role": "research",
        "goal": "Compare suitable local AI models.",
        "steps": [
            "Identify candidate models.",
            "Compare quality and performance.",
        ],
        "risks": [
            "Benchmark coverage may be limited.",
        ],
        "success_criteria": [
            "A ranked comparison is produced.",
        ],
    }
    plan.update(overrides)
    return plan


def test_valid_plan():
    client = FakeOllamaClient(
        [json.dumps(valid_plan())]
    )
    planner = LLMPlanner(
        ollama=client,
        model="test-model",
    )

    result = planner.classify(
        "Research local AI models"
    )

    assert result["planner_type"] == "llm"
    assert result["planner_attempts"] == 1
    assert result["fallback_reason"] is None
    assert result["primary_role"] == "research"
    assert result["needs"]["research"] is True
    assert result["query"] == "Research local AI models"
    assert len(client.calls) == 1
    assert client.calls[0]["kwargs"]["model"] == "test-model"


def test_markdown_fenced_json():
    response = (
        "```json\n"
        + json.dumps(valid_plan())
        + "\n```"
    )
    client = FakeOllamaClient([response])
    planner = LLMPlanner(ollama=client)

    result = planner.classify(
        "Research local AI models"
    )

    assert result["planner_type"] == "llm"
    assert result["planner_attempts"] == 1
    assert result["primary_role"] == "research"


def test_retry_succeeds():
    client = FakeOllamaClient(
        [
            "not valid JSON",
            json.dumps(valid_plan()),
        ]
    )
    planner = LLMPlanner(
        ollama=client,
        max_attempts=2,
    )

    result = planner.classify(
        "Research local AI models"
    )

    assert result["planner_type"] == "llm"
    assert result["planner_attempts"] == 2
    assert result["fallback_reason"] is None
    assert len(client.calls) == 2

    first_prompt = client.calls[0]["prompt"]
    second_prompt = client.calls[1]["prompt"]

    assert first_prompt != second_prompt
    assert "Your previous response was rejected" in second_prompt
    assert "PlanValidationError" in second_prompt
    assert "not valid JSON" in second_prompt


def test_both_attempts_fail():
    client = FakeOllamaClient(
        [
            "invalid response one",
            "invalid response two",
        ]
    )
    planner = LLMPlanner(
        ollama=client,
        max_attempts=2,
    )

    result = planner.classify(
        "Build a Python API"
    )

    assert result["planner_type"] == "deterministic_fallback"
    assert result["planner_attempts"] == 2
    assert result["primary_role"] == "developer"
    assert "attempt 1" in result["fallback_reason"]
    assert "attempt 2" in result["fallback_reason"]
    assert "PlanValidationError" in result["fallback_reason"]
    assert len(client.calls) == 2


def test_invalid_role_uses_fallback():
    response = valid_plan(
        primary_role="unsupported_role"
    )
    client = FakeOllamaClient(
        [json.dumps(response)]
    )
    planner = LLMPlanner(
        ollama=client,
        max_attempts=1,
    )

    result = planner.classify(
        "Research local AI models"
    )

    assert result["planner_type"] == "deterministic_fallback"
    assert result["planner_attempts"] == 1
    assert result["primary_role"] == "research"
    assert "Unsupported primary role" in result["fallback_reason"]


def test_ollama_failure_uses_fallback():
    client = FakeOllamaClient(
        [ConnectionError("Ollama unavailable")]
    )
    planner = LLMPlanner(
        ollama=client,
        max_attempts=1,
    )

    result = planner.classify(
        "Organize my Obsidian notes"
    )

    assert result["planner_type"] == "deterministic_fallback"
    assert result["planner_attempts"] == 1
    assert result["primary_role"] == "second_brain"
    assert "ConnectionError" in result["fallback_reason"]


def test_invalid_max_attempts():
    try:
        LLMPlanner(max_attempts=0)
    except ValueError as error:
        assert str(error) == "max_attempts must be at least 1."
    else:
        raise AssertionError(
            "max_attempts=0 should raise ValueError."
        )


def test_empty_query_is_rejected():
    client = FakeOllamaClient([])
    planner = LLMPlanner(ollama=client)

    try:
        planner.classify("   ")
    except ValueError as error:
        assert str(error) == "Query cannot be empty."
    else:
        raise AssertionError(
            "Empty query should raise ValueError."
        )

    assert len(client.calls) == 0

def test_deterministic_guardrails_preserve_explicit_roles():
    client = FakeOllamaClient(
        [json.dumps(valid_plan())]
    )
    planner = LLMPlanner(ollama=client)

    result = planner.classify(
        "Research local AI models and build a Python benchmark."
    )

    assert result["planner_type"] == "llm"
    assert result["needs"]["research"] is True
    assert result["needs"]["developer"] is True
    assert "research" in result["guardrail_roles"]
    assert "developer" in result["guardrail_roles"]

def test_ce_alias_is_normalized_to_ceo():
    response = valid_plan(
        needs={
            "memory": True,
            "developer": False,
            "research": False,
            "second_brain": False,
            "trading": False,
            "ceo": False,
        },
        primary_role="ce",
        goal="Identify the next project milestone.",
        steps=[
            "Review the current project state.",
            "Select the next incomplete milestone.",
        ],
        risks=[
            "Historical memory may contain outdated status.",
        ],
        success_criteria=[
            "The next milestone is identified.",
        ],
    )

    client = FakeOllamaClient(
        [json.dumps(response)]
    )
    planner = LLMPlanner(
        ollama=client,
        max_attempts=2,
    )

    result = planner.classify(
        "What should I prioritize next?"
    )

    assert result["planner_type"] == "llm"
    assert result["planner_attempts"] == 1
    assert result["primary_role"] == "ceo"
    assert result["needs"]["ceo"] is True
    assert result["primary_role_needs_correction"] is True
    assert result["role_correction"] == {
        "from": "ce",
        "to": "ceo",
    }
    assert result["fallback_reason"] is None
    assert len(client.calls) == 1