"""
Current-state provider for AI-OS.

Exposes the project's current state in a reusable form for the
execution pipeline, diagnostics, and future planning components.
"""

from copy import deepcopy
from typing import Any, Dict

from brain.state.current import CURRENT_STATE


class StateProvider:
    def snapshot(self) -> Dict[str, Any]:
        """
        Return an isolated copy so Pipeline stages cannot accidentally
        modify the global state dictionary.
        """
        return deepcopy(CURRENT_STATE)

    def format_context(self, state: Dict[str, Any]) -> str:
        modules = state.get("modules", {})
        services = state.get("services", {})

        module_lines = [
            f"- {name}: {status}"
            for name, status in modules.items()
        ]

        service_lines = [
            f"- {name}: {'running/configured' if enabled else 'unavailable'}"
            for name, enabled in services.items()
        ]

        return "\n".join(
            [
                f"Project: {state.get('project', 'AI-OS')}",
                f"Version: {state.get('version', 'unknown')}",
                f"Current focus: {state.get('current_focus', 'unknown')}",
                f"Next focus: {state.get('next_focus', 'unknown')}",
                "",
                "Modules:",
                *module_lines,
                "",
                "Services:",
                *service_lines,
            ]
        )