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
assert "Current focus:" in context
assert "Next focus:" in context

print("\nState Provider test passed.")