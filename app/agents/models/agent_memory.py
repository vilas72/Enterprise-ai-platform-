"""
Agent memory snapshot.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentMemory:
    """
    Snapshot of memory available during agent execution.
    """

    short_term: list[str] = field(
        default_factory=list
    )

    long_term: list[str] = field(
        default_factory=list
    )

    semantic: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def is_empty(self) -> bool:
        return (
            not self.short_term
            and not self.long_term
            and not self.semantic
        )