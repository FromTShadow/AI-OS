from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(
    "localhost",
    port=6333,
    check_compatibility=False
)

client.recreate_collection(
    collection_name="obsidian_memory",
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    )
)

print("Collection created successfully!")