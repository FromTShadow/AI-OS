from brain.benchmarks.model_benchmark import ModelBenchmark


benchmark = ModelBenchmark(
    model="qwen3.5:4b",
)

cases = benchmark.cases()

assert len(cases) == 4
assert {case.name for case in cases} == {
    "planning",
    "coding",
    "research",
    "reasoning",
}

print("=" * 60)
print("AI-OS MODEL BENCHMARK")
print("=" * 60)

results = benchmark.run()

total_duration = 0.0

for result in results:
    total_duration += result.duration_seconds

    print()
    print(f"Model: {result.model}")
    print(f"Case: {result.case_name}")
    print(f"Duration: {result.duration_seconds}s")
    print(f"Output characters: {result.output_characters}")
    print("-" * 40)
    print(result.response[:500])

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

for result in results:
    print(
        f"{result.case_name}: "
        f"{result.duration_seconds}s | "
        f"{result.output_characters} chars"
    )

print(f"\nTotal duration: {round(total_duration, 3)}s")

assert all(result.response for result in results)
assert all(result.duration_seconds > 0 for result in results)

print("\nModel Benchmark test passed.")