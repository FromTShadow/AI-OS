"""
AI Brain response engine.
Combines planning, memory retrieval, Ollama generation, and source tracking.
"""

from brain.memory.search import MemorySearch
from brain.models.ollama import OllamaClient
from brain.planner.planner import Planner


class AIBrain:
    def __init__(self):
        self.memory = MemorySearch()
        self.ollama = OllamaClient()
        self.planner = Planner()

    def retrieve_memory(self, query: str, limit: int = 5):
        return self.memory.search(query, limit=limit)

    def build_context(self, results) -> str:
        if not results:
            return "No relevant memory found."

        context_blocks = []

        for i, result in enumerate(results, start=1):
            title = result.payload.get("title", "Untitled")
            folder = result.payload.get("folder", "Unknown")
            chunk_index = result.payload.get("chunk_index", 0)
            content = result.payload.get("content", "")

            context_blocks.append(
                f"[Memory {i}]\n"
                f"Title: {title}\n"
                f"Folder: {folder}\n"
                f"Chunk: {chunk_index}\n"
                f"Content:\n{content}"
            )

        return "\n\n---\n\n".join(context_blocks)

    def format_plan(self, plan: dict) -> str:
        needs = plan["needs"]

        active_roles = [
            role for role, needed in needs.items()
            if needed and role != "memory"
        ]

        if not active_roles:
            active_roles = ["ceo"]

        return (
            f"Primary role: {plan['primary_role']}\n"
            f"Specialists needed: {', '.join(active_roles)}\n"
            f"Memory needed: {needs.get('memory', False)}"
        )

    def format_sources(self, results) -> str:
        if not results:
            return "No memory sources used."

        lines = []

        for i, result in enumerate(results, start=1):
            title = result.payload.get("title", "Untitled")
            folder = result.payload.get("folder", "Unknown")
            score = round(result.score, 3)
            chunk_index = result.payload.get("chunk_index", 0)
            confidence = self.memory.confidence_label(result.score)

            lines.append(
                f"{i}. {title} | "
                f"folder: {folder} | "
                f"chunk: {chunk_index} | "
                f"score: {score} | "
                f"confidence: {confidence}"
            )

        return "\n".join(lines)

    def answer(self, query: str) -> str:
        plan = self.planner.classify(query)
        results = self.retrieve_memory(query)
        context = self.build_context(results)
        plan_report = self.format_plan(plan)

        prompt = f"""
You are the AI Brain for Nejc's local AI Operating System.

You have created this execution plan:

{plan_report}

Use the memory context below to answer the user's question.
Adapt your answer to the primary role:
- developer: practical technical implementation
- research: structured research and comparison
- second_brain: organization, notes, knowledge management
- trading: systematic trading, testing, risk management
- ceo: priorities, roadmap, ROI, decision-making

If the context is not enough, say what is missing.

Memory Context:
{context}

User Question:
{query}

Answer clearly and practically.
"""

        answer = self.ollama.chat(prompt)
        sources = self.format_sources(results)

        return (
            f"{answer}\n\n"
            f"---\n"
            f"Brain plan:\n{plan_report}\n\n"
            f"Memory sources used:\n{sources}"
        )