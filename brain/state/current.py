"""
Current runtime state for AI-OS.

Unlike semantic memory, this file represents the CURRENT
status of the project.

It should always describe reality, not historical notes.
"""

CURRENT_STATE = {
    "project": "AI-OS",

    "version": "0.3.2-dev",

    "git_commit": "1db052a",

    "modules": {
        "planner": "complete",
        "pipeline": "complete",
        "memory_search": "complete",
        "memory_compressor": "needs_improvement",
        "context_builder": "in_progress",
        "prompt_loader": "complete",
        "router": "complete",
        "state_provider": "complete",
        "llm_planner": "planned",
        "multi_agent": "planned",
    },

    "services": {
        "ollama": True,
        "qdrant": True,
        "postgres": True,
        "n8n": True,
        "open_webui": True,
    },

    "current_focus": "Context authority and state priority",

    "next_focus": "Memory compression and pipeline tests",
}