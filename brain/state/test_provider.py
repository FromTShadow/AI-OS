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

assert state["current_focus"] == "Pipeline testing and observability"
assert state["next_focus"] == "LLM Planner preparation"

assert "Current focus:" in context
assert "Next focus:" in context

print("\nState Provider test passed.")