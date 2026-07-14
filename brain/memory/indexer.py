"""
Memory indexer for AI-OS Brain.
Indexes Obsidian Markdown notes into Qdrant using chunked storage.
"""

from pathlib import Path
import hashlib

from qdrant_client.models import PointStruct

from brain.config.settings import VAULT_PATH, COLLECTION_NAME
from brain.memory.client import QdrantMemoryClient
from brain.memory.chunking import TextChunker
from brain.models.ollama import OllamaClient


class MemoryIndexer:
    def __init__(self):
        self.memory = QdrantMemoryClient()
        self.ollama = OllamaClient()
        self.chunker = TextChunker()

    def make_id(self, path: Path, chunk_index: int) -> int:
        raw_id = f"{path}:{chunk_index}"
        digest = hashlib.md5(raw_id.encode("utf-8")).hexdigest()
        return int(digest[:16], 16)

    def get_markdown_notes(self) -> list[Path]:
        return list(VAULT_PATH.rglob("*.md"))

    def index_note(self, note_path: Path):
        text = note_path.read_text(encoding="utf-8").strip()

        if not text:
            return []

        chunks = self.chunker.chunk_text(text)
        relative_path = note_path.relative_to(VAULT_PATH)

        points = []

        for chunk_index, chunk in enumerate(chunks):
            embedding = self.ollama.embed(chunk)

            points.append(
                PointStruct(
                    id=self.make_id(note_path, chunk_index),
                    vector=embedding,
                    payload={
                        "title": note_path.stem,
                        "path": str(note_path),
                        "relative_path": str(relative_path),
                        "folder": str(relative_path.parent),
                        "chunk_index": chunk_index,
                        "chunk_count": len(chunks),
                        "content": chunk,
                    },
                )
            )

        self.memory.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

        return relative_path, len(chunks)

    def index_all_notes(self):
        indexed = []

        for note_path in self.get_markdown_notes():
            result = self.index_note(note_path)

            if result:
                relative_path, chunk_count = result
                indexed.append(result)
                print(f"Indexed: {relative_path} ({chunk_count} chunks)")

        print(f"Indexed {len(indexed)} notes.")
        return indexed