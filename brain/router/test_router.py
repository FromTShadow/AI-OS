from brain.execution.task import Task
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
    task = Task(query=query)
    task.plan = planner.classify(query)

    task = router.route(task)

    print("\n" + "=" * 60)
    print("Query:", task.query)
    print("Primary role:", task.primary_role)
    print("Specialists:", task.specialists)
    print(
        "System prompt:",
        task.system_prompt.name,
        task.system_prompt.version,
    )
    print(
        "Specialist prompt:",
        task.specialist_prompt.name,
        task.specialist_prompt.version,
    )
    print("Prompt versions:", task.prompt_versions)

    assert task.primary_role == task.plan["primary_role"]
    assert task.specialist_prompt.name == task.primary_role
    assert task.system_prompt.content
    assert task.specialist_prompt.content
    assert task.metadata["route"]["primary_role"] == task.primary_role

print("\nTask-based Router test passed.")