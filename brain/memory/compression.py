"""
Deterministic memory compression for AI-OS.

The compressor selects the most query-relevant passages from retrieved
memory instead of sending every complete note to the language model.
"""

import re
from dataclasses import dataclass
from typing import Any, Iterable, List, Set


@dataclass
class CompressedMemory:
    context: str
    source_count: int
    original_characters: int
    compressed_characters: int


class MemoryCompressor:
    def __init__(
        self,
        max_total_characters: int = 2200,
        max_characters_per_source: int = 350,
    ):
        if max_total_characters <= 0:
            raise ValueError("max_total_characters must be greater than zero.")

        if max_characters_per_source <= 0:
            raise ValueError(
                "max_characters_per_source must be greater than zero."
            )

        self.max_total_characters = max_total_characters
        self.max_characters_per_source = max_characters_per_source

    def tokenize(self, text: str) -> Set[str]:
        return {
            token
            for token in re.findall(r"[a-zA-Z0-9_-]+", text.lower())
            if len(token) >= 3
        }

    def split_passages(self, text: str) -> List[str]:
        """
        Split Markdown into paragraph-sized passages.
        """
        passages = re.split(r"\n\s*\n+", text.strip())

        return [
            passage.strip()
            for passage in passages
            if passage.strip()
        ]

    def passage_score(
        self,
        passage: str,
        query_tokens: Set[str],
        position: int,
    ) -> float:
        passage_tokens = self.tokenize(passage)

        if not passage_tokens:
            return 0.0

        overlap = len(query_tokens.intersection(passage_tokens))
        coverage = overlap / max(len(query_tokens), 1)

        # Slightly prefer earlier passages because headings and summaries
        # commonly appear near the beginning of Obsidian notes.
        position_bonus = max(0.0, 0.15 - (position * 0.01))

        return coverage + position_bonus

    def select_content(self, text: str, query: str) -> str:
        passages = self.split_passages(text)

        if not passages:
            return ""

        query_tokens = self.tokenize(query)

        ranked = sorted(
            enumerate(passages),
            key=lambda item: self.passage_score(
                passage=item[1],
                query_tokens=query_tokens,
                position=item[0],
            ),
            reverse=True,
        )

        selected = []
        current_length = 0

        for original_position, passage in ranked:
            added_length = len(passage) + 2

            if current_length + added_length > self.max_characters_per_source:
                continue

            selected.append((original_position, passage))
            current_length += added_length

        if not selected:
            return passages[0][: self.max_characters_per_source]

        # Restore original document order after relevance selection.
        selected.sort(key=lambda item: item[0])

        return "\n\n".join(
            passage for _, passage in selected
        )

    def compress(
        self,
        query: str,
        results: Iterable[Any],
    ) -> CompressedMemory:
        result_list = list(results)

        original_characters = sum(
            len((result.payload or {}).get("content", ""))
            for result in result_list
        )

        blocks = []
        total_characters = 0
        included_sources = 0

        for index, result in enumerate(result_list, start=1):
            payload = result.payload or {}

            content = self.select_content(
                text=payload.get("content", ""),
                query=query,
            )

            if not content:
                continue

            title = payload.get("title", "Untitled")
            folder = payload.get("folder", "Unknown")

            block = (
                f"[Memory {index}] {title} | {folder}\n"
                f"{content}"
)

            if (
                total_characters + len(block)
                > self.max_total_characters
            ):
                break

            blocks.append(block)
            total_characters += len(block)
            included_sources += 1

        context = (
            "\n\n---\n\n".join(blocks)
            if blocks
            else "No relevant memory was retrieved."
        )

        return CompressedMemory(
            context=context,
            source_count=included_sources,
            original_characters=original_characters,
            compressed_characters=len(context),
        )