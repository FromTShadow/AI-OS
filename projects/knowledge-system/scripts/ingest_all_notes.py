from pathlib import Path
import hashlib
import requests

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

VAULT_PATH = Path.home() / "AI-OS" / "vault"
COLLECTION_NAME = "obsidian_memory"

client = QdrantClient(
    "localhost",
    port=6333,
    check_compatibility=False
)

def make_id(path: Path) -> int:
    digest = hashlib.md5(str(path).encode("utf-8")).hexdigest()
    return int(digest[:16], 16)

def embed_text(text: str):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]

points = []
notes = list(VAULT_PATH.rglob("*.md"))

for note_path in notes:
    text = note_path.read_text(encoding="utf-8").strip()

    if not text:
        continue

    embedding = embed_text(text)

    relative_path = note_path.relative_to(VAULT_PATH)

    points.append(
        PointStruct(
            id=make_id(note_path),
            vector=embedding,
            payload={
                "title": note_path.stem,
                "path": str(note_path),
                "relative_path": str(relative_path),
                "folder": str(relative_path.parent),
                "content": text
            }
        )
    )

    print(f"Prepared: {relative_path}")

if points:
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

print(f"Stored {len(points)} notes in Qdrant.")