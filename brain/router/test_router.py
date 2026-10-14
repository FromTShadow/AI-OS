from brain.execution.task import Task
from brain.planner.planner import Planner
from brain.router.router import SpecialistRouter


def test_router_assigns_prompts_and_metadata():
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

        assert task.primary_role == task.plan["primary_role"]
        assert task.specialist_prompt.name == task.primary_role
        assert task.system_prompt.content
        assert task.specialist_prompt.content
        assert task.metadata["route"]["primary_role"] == task.primary_role


def test_router_preserves_prompt_version_metadata():
    planner = Planner()
    router = SpecialistRouter()

    task = Task(query="Research local AI models")
    task.plan = planner.classify(task.query)
    task = router.route(task)

    assert task.prompt_versions
    assert task.prompt_versions["system"] == task.system_prompt.version
    assert (
        task.prompt_versions[task.primary_role]
        == task.specialist_prompt.version
    )
