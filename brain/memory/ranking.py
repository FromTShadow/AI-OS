"""
Deterministic memory reranking for AI-OS.

The ranker sits after semantic retrieval and before compression.
It combines Qdrant semantic similarity with lightweight metadata
and lexical relevance signals.
"""

import re
from typing import Any, List, Set


class MemoryRanker:
    def tokenize(self, text: str) -> Set[str]:
        return {
            token
            for token in re.findall(r"[a-zA-Z0-9_-]+", text.lower())
            if len(token) >= 3
        }

    def lexical_score(self, query: str, result: Any) -> float:
        payload = result.payload or {}

        searchable_text = " ".join(
            [
                payload.get("title", ""),
                payload.get("folder", ""),
                payload.get("content", ""),
            ]
        )

        query_tokens = self.tokenize(query)
        memory_tokens = self.tokenize(searchable_text)

        if not query_tokens:
            return 0.0

        overlap = len(query_tokens.intersection(memory_tokens))
        return overlap / len(query_tokens)

    def metadata_score(self, query: str, result: Any) -> float:
        """
        Apply small, explainable bonuses/penalties based on memory type.

        This is intentionally conservative. Semantic similarity remains
        the strongest signal.
        """
        payload = result.payload or {}

        title = payload.get("title", "").lower()
        folder = payload.get("folder", "").lower()
        query_tokens = self.tokenize(query)

        score = 0.0

        # Project-level questions benefit from project documentation.
        project_terms = {
            "project",
            "prioritize",
            "priority",
            "next",
            "roadmap",
            "architecture",
            "module",
            "ai-os",
        }

        if query_tokens.intersection(project_terms):
            if "project" in folder:
                score += 0.10

            if "ai-os" in title or "ai_os" in title:
                score += 0.10

        # Agent definition notes are often useful for role information,
        # but less useful for general project-status questions.
        if title.endswith("-agent") or "ai-agents" in folder:
            score -= 0.08

        return score

    def score(self, query: str, result: Any) -> float:
        semantic = float(result.score or 0.0)
        lexical = self.lexical_score(query, result)
        metadata = self.metadata_score(query, result)

        return (
            semantic * 0.70
            + lexical * 0.30
            + metadata
        )

    def rank(
        self,
        query: str,
        results: List[Any],
        limit: int = 5,
    ) -> List[Any]:
        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        ranked = sorted(
            results,
            key=lambda result: self.score(query, result),
            reverse=True,
        )

        return ranked[:limit]