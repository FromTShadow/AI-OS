from brain.models.ollama import OllamaClient

ollama = OllamaClient()

print("Health:", ollama.health())
print("Models:", ollama.list_models())

embedding = ollama.embed("AI-OS memory test")
print("Embedding length:", len(embedding))

answer = ollama.chat("Say hello in one short sentence.")
print("Chat response:", answer)