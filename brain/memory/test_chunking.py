from brain.memory.chunking import TextChunker


def test_chunk_text_splits_long_text():
    text = "This is a test note for AI-OS memory. " * 200
    chunker = TextChunker(chunk_size=500, overlap=100)

    chunks = chunker.chunk_text(text)

    assert len(chunks) > 1
    assert all(chunks)
    assert all(len(chunk) <= 500 for chunk in chunks)


def test_chunk_text_returns_short_text_as_one_chunk():
    text = "A short memory note."
    chunker = TextChunker(chunk_size=500, overlap=100)

    assert chunker.chunk_text(text) == [text]


def test_chunk_text_returns_empty_list_for_whitespace():
    chunker = TextChunker(chunk_size=500, overlap=100)

    assert chunker.chunk_text("   \n\t  ") == []
