"""
Semantic memory search for AI-OS Brain.

Searches Qdrant using Ollama embeddings, removes duplicate points,
and keeps only the strongest chunk from each note.
"""

from typing import Any, List

from brain.config.settings import COLLECTION_NAME
from brain.memory.client import QdrantMemoryClient
from brain.models.ollama import OllamaClient


class MemorySearch:
    def __init__(self):
        self.memory = QdrantMemoryClient()
        self.ollama = OllamaClient()

    def raw_search(self, query: str, limit: int = 20) -> List[Any]:
        query_embedding = self.ollama.embed(query)

        results = self.memory.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
        )

        return results.points

    def candidates(self, query: str, limit: int = 15) -> List[Any]:
        raw_results = self.raw_search(
            query,
            limit=max(limit * 4, 20),
        )

        unique_notes = self.group_by_note(raw_results)

        return unique_notes[:limit]


    def note_key(self, result: Any) -> str:
        payload = result.payload or {}

        return (
            payload.get("relative_path")
            or payload.get("path")
            or payload.get("title")
            or str(result.id)
        )

    def group_by_note(self, results: List[Any]) -> List[Any]:
        """
        Keep only the highest-scoring chunk from each source note.
        """
        best_by_note = {}

        for result in results:
            key = self.note_key(result)
            current = best_by_note.get(key)

            if current is None or result.score > current.score:
                best_by_note[key] = result

        unique_results = list(best_by_note.values())
        unique_results.sort(key=lambda item: item.score, reverse=True)

        return unique_results

    def confidence_label(self, score: float) -> str:
        if score >= 0.70:
            return "High"

        if score >= 0.55:
            return "Medium"

        return "Low"

    def search(self, query: str, limit: int = 5) -> List[Any]:
        return self.candidates(
            query=query,
            limit=limit,
        )