from qdrant_client import QdrantClient

client = QdrantClient(
    "localhost",
    port=6333,
    check_compatibility=False
)

points, _ = client.scroll(
    collection_name="obsidian_memory",
    limit=10
)

for point in points:
    print(point.payload["title"])