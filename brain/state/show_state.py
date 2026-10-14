from brain.state.current import CURRENT_STATE

print("\nAI-OS State\n")

print("Version:", CURRENT_STATE["version"])
print("Current focus:", CURRENT_STATE["current_focus"])
print("Next focus:", CURRENT_STATE["next_focus"])

print("\nModules")

for module, status in CURRENT_STATE["modules"].items():
    print(f"  {module:20} {status}")

print("\nServices")

for service, status in CURRENT_STATE["services"].items():
    print(f"  {service:20} {status}")