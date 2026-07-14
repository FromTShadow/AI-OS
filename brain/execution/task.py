"""
Task state for the AI-OS execution pipeline.

A Task carries one user request through planning, memory retrieval,
context construction, model execution, and response formatting.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    query: str

    plan: Dict[str, Any] = field(default_factory=dict)
    memory_results: List[Any] = field(default_factory=list)

    context: str = ""
    prompt: str = ""
    answer: str = ""

    primary_role: Optional[str] = None
    specialists: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)