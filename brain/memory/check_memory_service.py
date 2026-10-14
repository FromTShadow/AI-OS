from brain.memory.client import QdrantMemoryClient
from brain.memory.search import MemorySearch

memory_client = QdrantMemoryClient()

print("Qdrant health:", memory_client.health())
print("Collections:", memory_client.collections())

search = MemorySearch()

results = search.search("project priorities", limit=3)

for result in results:
    print("\n====================")
    print("Score:", round(result.score, 3))
    print("Title:", result.payload.get("title"))
    print("Folder:", result.payload.get("folder"))