from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

print("Connected to Qdrant!")

collections = client.get_collections()

print(collections)