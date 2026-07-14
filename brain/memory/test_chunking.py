from brain.memory.chunking import TextChunker

text = """
This is a test note for AI-OS memory.
""" * 200

chunker = TextChunker(chunk_size=500, overlap=100)

chunks = chunker.chunk_text(text)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print("\n--- Chunk", i, "---")
    print(chunk[:200])