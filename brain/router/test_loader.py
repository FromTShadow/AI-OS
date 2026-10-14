from brain.router.loader import PromptLoader


def test_prompt_loader_loads_versioned_bundle():
    loader = PromptLoader()

    bundle = loader.load_bundle("developer")
    system_prompt = bundle["system"]
    developer_prompt = bundle["specialist"]

    assert system_prompt.version == "1.0.0"
    assert developer_prompt.version == "1.0.0"
    assert system_prompt.content
    assert developer_prompt.content
    assert system_prompt.name
    assert developer_prompt.name


def test_prompt_loader_lists_available_prompts():
    loader = PromptLoader()

    available = loader.available_prompts()

    assert available
    assert "developer" in available
