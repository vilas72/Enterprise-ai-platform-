from __future__ import annotations

from app.memory.token_budget_manager import TokenBudgetManager


class SlidingWindowMemory:
    """Placeholder sliding-window memory component."""

    def __init__(self, token_budget_manager: TokenBudgetManager) -> None:
        self._token_budget_manager = token_budget_manager

    async def retrieve(self, conversation_id: str) -> list[str]:
        return []
