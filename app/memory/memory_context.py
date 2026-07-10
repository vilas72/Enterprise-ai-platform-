from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MemoryContext:
    """Represents the memory context that can be injected into prompts."""

    summary: str | None = None
    recent_messages: list[str] = field(default_factory=list)
    semantic_memories: list[str] = field(default_factory=list)
    token_count: int = 0
