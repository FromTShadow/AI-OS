import requests

text = """
AI Operating System

Goal:
Build a local AI ecosystem that acts as:
- Personal Second Brain
- Research Assistant
- Website Development Assistant
- Trading Bot Assistant
"""

response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": text
    }
)

data = response.json()

print("Embedding length:", len(data["embedding"]))