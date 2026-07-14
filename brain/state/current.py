"""
Current runtime state for AI-OS.

Unlike semantic memory, this file represents the CURRENT
status of the project.

It should always describe reality, not historical notes.
"""

CURRENT_STATE = {

    "project": "AI-OS",

    "version": "0.3.1-dev",

    "git_commit": "bea4fed",

    "modules": {

        "planner": "complete",

        "pipeline": "complete",

        "memory_search": "complete",

        "context_builder": "complete",

        "router": "planned",

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

    "current_focus": "State Module",

    "next_focus": "Router",

}