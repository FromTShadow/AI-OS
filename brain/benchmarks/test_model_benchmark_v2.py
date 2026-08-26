from brain.benchmarks.model_benchmark_v2 import BenchmarkCasesV2


benchmark = BenchmarkCasesV2()

cases = benchmark.cases()

print("Total cases:", len(cases))

for case in cases:
    print(
        case.category,
        "->",
        case.name,
    )


assert len(cases) == 12

categories = {
    case.category
    for case in cases
}

assert categories == {
    "planning",
    "coding",
    "research",
    "reasoning",
}

for category in categories:
    count = sum(
        1
        for case in cases
        if case.category == category
    )

    assert count == 3


print("\nBenchmark V2 structure test passed.")