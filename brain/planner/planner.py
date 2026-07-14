"""
AI Brain Planner.
Decides what type of task the user is asking for.
"""


class Planner:
    def classify(self, query: str) -> dict:
        q = query.lower()

        needs = {
            "memory": True,
            "developer": False,
            "research": False,
            "second_brain": False,
            "trading": False,
            "ceo": False,
        }

        if any(word in q for word in ["code", "website", "app", "api", "python", "fastapi", "debug", "build"]):
            needs["developer"] = True

        if any(word in q for word in ["research", "compare", "analyze", "paper", "article", "summarize"]):
            needs["research"] = True

        if any(word in q for word in ["obsidian", "note", "organize", "second brain", "knowledge"]):
            needs["second_brain"] = True

        if any(word in q for word in ["trading", "bot", "strategy", "backtest", "market", "crypto"]):
            needs["trading"] = True

        if any(word in q for word in ["priority", "roadmap", "business", "roi", "what should i do"]):
            needs["ceo"] = True

        if not any([needs["developer"], needs["research"], needs["second_brain"], needs["trading"], needs["ceo"]]):
            needs["ceo"] = True

        return {
            "query": query,
            "needs": needs,
            "primary_role": self.primary_role(needs),
        }

    def primary_role(self, needs: dict) -> str:
        priority = [
            "developer",
            "research",
            "second_brain",
            "trading",
            "ceo",
        ]

        for role in priority:
            if needs.get(role):
                return role

        return "ceo"