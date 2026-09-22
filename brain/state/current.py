"""
Current runtime state for AI-OS.

Unlike semantic memory, this file represents the CURRENT
status of the project.

It should always describe reality, not historical notes.
"""

CURRENT_STATE = {
    "project": "AI-OS",

    "version": "0.3.5-dev",


    "modules": {
        "memory_ranker": "complete",
        "memory_compressor": "complete",
        "context_builder": "complete",
        "planner": "complete",
        "pipeline": "complete",
        "memory_search": "complete",
        "prompt_loader": "complete",
        "router": "complete",
        "state_provider": "complete",
        "model_benchmark_v3": "complete",
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

    "current_focus": "LLM Planner preparation",
    "next_focus": "LLM Planner prototype",
}