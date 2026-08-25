from brain.memory.compression import MemoryCompressor
from brain.memory.search import MemorySearch

query = "What should I prioritize next in my AI OS project?"

search = MemorySearch()
results = search.search(query, limit=5)

compressor = MemoryCompressor()

compressed = compressor.compress(
    query=query,
    results=results,
)

print("=" * 60)
print("COMPRESSION REPORT")
print("=" * 60)

print("Retrieved results:", len(results))
print("Included sources:", compressed.source_count)
print("Original characters:", compressed.original_characters)
print("Compressed characters:", compressed.compressed_characters)

if compressed.original_characters:
    reduction = (
        1
        - compressed.compressed_characters
        / compressed.original_characters
    ) * 100

    print("Reduction:", round(reduction, 1), "%")

print("\nCompressed context:\n")
print(compressed.context)

assert compressed.source_count > 0

assert compressed.compressed_characters < compressed.original_characters, (
    "Compression failed: output is not smaller than input."
)

assert (
    compressed.compressed_characters
    <= compressor.max_total_characters
), "Compression exceeded the configured character budget."

print("\nMemory Compressor test passed.")