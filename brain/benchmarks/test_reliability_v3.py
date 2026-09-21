from brain.benchmarks.reliability_v3 import (
    ReliabilityBenchmarkV3,
)


benchmark = ReliabilityBenchmarkV3(
    model="qwen3.5:4b",
    trials=3,
)

print("Model:", benchmark.model)
print("Trials:", benchmark.trials)

assert benchmark.model == "qwen3.5:4b"
assert benchmark.trials == 3

print("\nReliability V3 structure test passed.")