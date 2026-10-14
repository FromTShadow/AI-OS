from brain.benchmarks.quality_v2 import QualityEvaluatorV2


def test_quality_v2_rewards_reasoning_using_both_timings():
    evaluator = QualityEvaluatorV2()

    good_result = evaluator.evaluate(
        case_name="reasoning",
        response=(
            "Model generation is the bottleneck. Retrieval takes 0.6 "
            "seconds while model generation takes 80 seconds, so generation "
            "should be optimized first."
        ),
    )

    bad_result = evaluator.evaluate(
        case_name="reasoning",
        response="The model takes 80 seconds. We should optimize performance.",
    )

    assert good_result.score == 100.0
    assert "uses_both_timings" in good_result.passed_checks

    assert bad_result.score < 100.0
    assert "uses_both_timings" in bad_result.failed_checks
    assert "correct_optimization_target" in bad_result.failed_checks


def test_quality_v2_checks_planning_priorities():
    evaluator = QualityEvaluatorV2()

    response = """
    The next priority should be the LLM Planner because it will improve
    task decomposition before multi-agent execution is introduced.

    After that, add pipeline tests before expanding the architecture.

    Finally, implement multi-agent execution once the foundation is stable.
    """

    result = evaluator.evaluate(
        case_name="planning_priorities",
        response=response,
    )

    assert result.score == 100.0
    assert "mentions_llm_planner" in result.passed_checks
    assert "mentions_multi_agent" in result.passed_checks