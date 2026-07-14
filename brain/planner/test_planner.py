from brain.planner.planner import Planner

planner = Planner()

queries = [
    "Build me a website for my AI OS",
    "Research best local AI models",
    "Organize my Obsidian notes",
    "Create a trading bot roadmap",
    "What should I prioritize next?",
]

for query in queries:
    plan = planner.classify(query)

    print("\nQuery:", query)
    print("Primary role:", plan["primary_role"])
    print("Needs:", plan["needs"])