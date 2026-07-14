from brain.router.loader import PromptLoader

loader = PromptLoader()

print("Available prompts:")

for prompt_name in loader.available_prompts():
    print("-", prompt_name)

bundle = loader.load_bundle("developer")

system_prompt = bundle["system"]
developer_prompt = bundle["specialist"]

print("\nSystem prompt:")
print("Name:", system_prompt.name)
print("Version:", system_prompt.version)
print("Description:", system_prompt.description)
print(system_prompt.content[:200])

print("\nDeveloper prompt:")
print("Name:", developer_prompt.name)
print("Version:", developer_prompt.version)
print("Description:", developer_prompt.description)
print(developer_prompt.content[:200])

assert system_prompt.version == "1.0.0"
assert developer_prompt.version == "1.0.0"
assert system_prompt.content
assert developer_prompt.content

print("\nVersioned Prompt Loader test passed.")