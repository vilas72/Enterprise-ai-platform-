from __future__ import annotations

from app.memory.memory_context import MemoryContext
from app.memory.semantic_memory import SemanticMemory
from app.memory.sliding_window_memory import SlidingWindowMemory
from app.memory.summary_memory import SummaryMemory
from app.memory.token_budget_manager import TokenBudgetManager


class MemoryManager:
    """Coordinates memory components for a conversation."""

    def __init__(
        self,
        conversation_service=None,
        sliding_window_memory: SlidingWindowMemory | None = None,
        summary_memory: SummaryMemory | None = None,
        semantic_memory: SemanticMemory | None = None,
        token_budget_manager: TokenBudgetManager | None = None,
    ) -> None:
        self._conversation_service = conversation_service
        self._sliding_window_memory = sliding_window_memory
        self._summary_memory = summary_memory
        self._semantic_memory = semantic_memory
        self._token_budget_manager = token_budget_manager or TokenBudgetManager()

    async def build_context(self, conversation_id: str) -> MemoryContext:
        """Build a lightweight memory context for a conversation."""
        recent_messages = []
        semantic_memories = []

        if self._sliding_window_memory is not None:
            recent_messages = await self._sliding_window_memory.retrieve(conversation_id)

        if self._semantic_memory is not None:
            semantic_memories = await self._semantic_memory.retrieve(conversation_id)

        summary = None
        if self._summary_memory is not None:
            summary = await self._summary_memory.retrieve(conversation_id)

        return MemoryContext(
            summary=summary,
            recent_messages=recent_messages,
            semantic_memories=semantic_memories,
            token_count=0,
        )
