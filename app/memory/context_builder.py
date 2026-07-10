from __future__ import annotations

from dataclasses import dataclass

from app.memory.memory_context import MemoryContext
from app.memory.memory_manager import MemoryManager


@dataclass(slots=True)
class ContextBuilder:
    """Builds the contextual memory payload for prompts."""

    memory_manager: MemoryManager

    async def build(self, conversation_id: str) -> MemoryContext:
        """Create the memory context for a conversation."""
        return await self.memory_manager.build_context(conversation_id)
