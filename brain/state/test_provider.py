from brain.state.provider import StateProvider

provider = StateProvider()

state = provider.snapshot()
context = provider.format_context(state)

print("=" * 60)
print("STATE PROVIDER TEST")
print("=" * 60)
print(context)

assert state["modules"]["memory_ranker"] == "complete"
assert state["modules"]["memory_compressor"] == "complete"
assert state["modules"]["context_builder"] == "complete"
assert state["modules"]["llm_planner"] == "complete"

assert state["version"] == "0.3.6-dev"
assert state["current_focus"] == "Multi-agent execution preparation"
assert state["next_focus"] == "Multi-agent execution prototype"

assert "Current focus:" in context
assert "Next focus:" in context

print("\nState Provider test passed.")