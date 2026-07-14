import requests
from qdrant_client import QdrantClient

query = input("Search: ")

response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": query
    }
)

query_embedding = response.json()["embedding"]

client = QdrantClient(
    "localhost",
    port=6333,
    check_compatibility=False
)

results = client.query_points(
    collection_name="obsidian_memory",
    query=query_embedding,
    limit=5
)

for result in results.points:
    print("\n====================")
    print("Score:", round(result.score, 3))
    print("Title:", result.payload["title"])
    print("Folder:", result.payload["folder"])
    print("====================")