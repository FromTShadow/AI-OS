"""
Reset Qdrant memory collection.
"""

from qdrant_client.models import VectorParams, Distance

from brain.config.settings import COLLECTION_NAME, VECTOR_SIZE
from brain.memory.client import QdrantMemoryClient


class MemoryReset:
    def __init__(self):
        self.memory = QdrantMemoryClient()

    def reset_collection(self):
        client = self.memory.client

        if client.collection_exists(COLLECTION_NAME):
            client.delete_collection(COLLECTION_NAME)

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        print(f"Reset collection: {COLLECTION_NAME}")