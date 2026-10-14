from brain.benchmarks.reliability_v3 import ReliabilityBenchmarkV3


def test_reliability_benchmark_configuration():
    benchmark = ReliabilityBenchmarkV3(
        model="qwen3.5:4b",
        trials=3,
    )

    assert benchmark.model == "qwen3.5:4b"
    assert benchmark.trials == 3