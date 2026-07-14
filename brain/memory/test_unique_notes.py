from brain.memory.search import MemorySearch

search = MemorySearch()

results = search.search(
    "What should I prioritize next in my AI OS project?",
    limit=5,
)

print("Unique results:", len(results))

seen = set()

for result in results:
    payload = result.payload or {}
    key = (
        payload.get("relative_path")
        or payload.get("path")
        or payload.get("title")
    )

    print(
        "-",
        payload.get("title", "Untitled"),
        "| path:",
        key,
        "| score:",
        round(result.score, 3),
    )

    if key in seen:
        raise RuntimeError(f"Duplicate note returned: {key}")

    seen.add(key)

print("No duplicate notes found.")