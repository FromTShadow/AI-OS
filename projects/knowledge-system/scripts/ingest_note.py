from pathlib import Path
import requests

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

NOTE_PATH = Path.home() / "AI-OS" / "vault" / "01-Projects" / "AI-OS.md"

text = NOTE_PATH.read_text(encoding="utf-8")

response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": text
    }
)

embedding = response.json()["embedding"]

client = QdrantClient(
    "localhost",
    port=6333,
    check_compatibility=False
)

client.upsert(
    collection_name="obsidian_memory",
    points=[
        PointStruct(
            id=1,
            vector=embedding,
            payload={
                "title": "AI-OS",
                "path": str(NOTE_PATH),
                "content": text
            }
        )
    ]
)

print("AI-OS note stored successfully!")