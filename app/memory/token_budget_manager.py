from __future__ import annotations


class TokenBudgetManager:
    """Simple token budget manager used by memory components."""

    def __init__(self, max_tokens: int = 4000) -> None:
        self.max_tokens = max_tokens

    def remaining(self, used_tokens: int) -> int:
        return max(self.max_tokens - used_tokens, 0)
