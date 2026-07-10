from __future__ import annotations

from abc import ABC, abstractmethod

from app.conversation.conversation import Conversation


class ConversationStore(ABC):
    """
    Abstract repository for Conversation persistence.
    """

    @abstractmethod
    async def create(self, conversation: Conversation) -> None:
        """Create and persist a new conversation."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        """Persist a conversation."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, conversation_id: str) -> Conversation | None:
        """Retrieve a conversation by its identifier."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, conversation_id: str) -> None:
        """Delete a conversation."""
        raise NotImplementedError

    @abstractmethod
    async def exists(self, conversation_id: str) -> bool:
        """Determine whether a conversation exists."""
        raise NotImplementedError

    @abstractmethod
    async def list(self, *, limit: int = 100, offset: int = 0) -> list[Conversation]:
        """Return a paginated list of conversations."""
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        """Return the total number of conversations."""
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        """Remove all conversations."""
        raise NotImplementedError