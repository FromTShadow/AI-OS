"""
Qdrant memory client for AI-OS Brain.
Handles connection to the vector database.
"""

from qdrant_client import QdrantClient

from brain.config.settings import QDRANT_HOST, QDRANT_PORT


class QdrantMemoryClient:
    def __init__(self, host: str = QDRANT_HOST, port: int = QDRANT_PORT):
        self.client = QdrantClient(
            host=host,
            port=port,
            check_compatibility=False,
        )

    def health(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False

    def collections(self):
        return self.client.get_collections()