from types import SimpleNamespace

import pytest

from brain.memory.compression import MemoryCompressor


def make_result(content, title="Test note", folder="Research"):
    return SimpleNamespace(
        payload={
            "content": content,
            "title": title,
            "folder": folder,
        }
    )


def test_compression_selects_relevant_content():
    compressor = MemoryCompressor(max_characters_per_source=100)

    result = make_result(
        "Unrelated material about cooking and gardening. " * 5
        + "\n\n"
        + "The AI-OS planner should prioritize reliable multi-agent "
        "execution and automated testing."
    )

    compressed = compressor.compress(
        query="AI-OS planner automated testing",
        results=[result],
    )

    assert compressed.source_count == 1
    assert "AI-OS planner" in compressed.context
    assert "Unrelated material" not in compressed.context


def test_compression_respects_total_character_budget():
    compressor = MemoryCompressor(
        max_total_characters=250,
        max_characters_per_source=150,
    )

    results = [
        make_result("AI-OS planner and testing information. " * 4),
        make_result("Memory retrieval and compression information. " * 4),
    ]

    compressed = compressor.compress(
        query="AI-OS memory testing",
        results=results,
    )

    assert compressed.compressed_characters <= 250
    assert len(compressed.context) == compressed.compressed_characters


def test_compression_reports_empty_results():
    compressor = MemoryCompressor()

    compressed = compressor.compress(
        query="AI-OS",
        results=[],
    )

    assert compressed.source_count == 0
    assert compressed.original_characters == 0
    assert compressed.context == "No relevant memory was retrieved."


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_total_characters": 0},
        {"max_total_characters": -1},
        {"max_characters_per_source": 0},
        {"max_characters_per_source": -1},
    ],
)
def test_compressor_rejects_invalid_limits(kwargs):
    with pytest.raises(ValueError):
        MemoryCompressor(**kwargs)
