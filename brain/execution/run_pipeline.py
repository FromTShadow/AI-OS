from brain.execution.pipeline import ExecutionPipeline

pipeline = ExecutionPipeline()

query = input("Ask Pipeline: ")

task = pipeline.execute(query)

print("\n" + "=" * 60)
print("PIPELINE RESULT")
print("=" * 60)

if task.errors:
    print("\nErrors:")

    for error in task.errors:
        print("-", error)
else:
    print("\nAnswer:")
    print(task.answer)

print("\nPlan:")
print(task.plan)

print("\nMetadata:")
print(task.metadata)

print("\nMemory sources:")

for result in task.memory_results:
    payload = result.payload or {}

    print(
        "-",
        payload.get("title", "Untitled"),
        "| folder:",
        payload.get("folder", "Unknown"),
        "| score:",
        round(result.score, 3),
    )