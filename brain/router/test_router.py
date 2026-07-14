from brain.planner.planner import Planner
from brain.router.router import SpecialistRouter

planner = Planner()
router = SpecialistRouter()

queries = [
    "Build a website for my AI OS",
    "Research the best local AI models",
    "Organize my Obsidian knowledge",
    "Create a trading bot roadmap",
    "What should I prioritize next?",
]

for query in queries:
    plan = planner.classify(query)
    route = router.route(plan)

    print("\n" + "=" * 60)
    print("Query:", query)
    print("Primary role:", route.primary_role)
    print("Specialists:", route.specialists)
    print(
        "System prompt:",
        route.system_prompt.name,
        route.system_prompt.version,
    )
    print(
        "Primary prompt:",
        route.primary_prompt.name,
        route.primary_prompt.version,
    )

    assert route.primary_role == plan["primary_role"]
    assert route.primary_prompt.name == route.primary_role
    assert route.primary_prompt.content

print("\nRouter test passed.")