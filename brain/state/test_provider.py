from brain.state.provider import StateProvider

provider = StateProvider()

state = provider.snapshot()
context = provider.format_context(state)

print("=" * 60)
print("STATE PROVIDER TEST")
print("=" * 60)
print(context)

assert state["project"] == "AI-OS"
assert state["modules"]["planner"] == "complete"
assert state["modules"]["router"] == "complete"
assert state["modules"]["state_provider"] == "complete"
assert state["current_focus"] == "Context authority and state priority"
assert state["next_focus"] == "Memory compression and pipeline tests"
assert "Current focus:" in context
assert "Next focus:" in context

print("\nState Provider test passed.")