from brain.benchmarks.quality_v3 import QualityEvaluatorV3


def test_quality_v3_accepts_valid_structured_responses():
    evaluator = QualityEvaluatorV3()

    planning_response = """
    {
      "priorities": [
        {
          "rank": 1,
          "name": "Improve benchmark quality",
          "rationale": "Reliable evaluation is needed before model routing.",
          "dependencies": [],
          "tradeoffs": ["Delays feature development"]
        },
        {
          "rank": 2,
          "name": "Build LLM Planner",
          "rationale": "Structured planning enables better orchestration.",
          "dependencies": ["Reliable model selection"],
          "tradeoffs": ["Adds another model call"]
        },
        {
          "rank": 3,
          "name": "Build multi-agent execution",
          "rationale": "Specialists can collaborate on complex tasks.",
          "dependencies": ["LLM Planner"],
          "tradeoffs": ["Higher complexity"]
        }
      ]
    }
    """

    reasoning_response = """
    {
      "bottleneck": "model_generation",
      "bottleneck_seconds": 75.0,
      "optimize_first": "model_generation",
      "reason": "Generation dominates the measured request latency."
    }
    """

    planning_result = evaluator.evaluate(
        "planning_priorities_structured",
        planning_response,
    )
    reasoning_result = evaluator.evaluate(
        "reasoning_bottleneck_structured",
        reasoning_response,
    )

    assert planning_result.score == 100.0
    assert reasoning_result.score == 100.0


def test_quality_v3_rejects_invalid_json():
    evaluator = QualityEvaluatorV3()

    result = evaluator.evaluate(
        "reasoning_bottleneck_structured",
        "This is not JSON.",
    )

    assert result.score == 0.0
    assert "valid_json" in result.failed_checks