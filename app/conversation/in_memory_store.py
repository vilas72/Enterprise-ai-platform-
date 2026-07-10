from __future__ import annotations

from threading import RLock

from app.conversation.conversation import Conversation
from app.conversation.conversation_store import ConversationStore


class InMemoryConversationStore(ConversationStore):
    """Thread-safe in-memory conversation store."""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._lock = RLock()

    async def create(self, conversation: Conversation) -> None:
        with self._lock:
            if conversation.conversation_id in self._conversations:
                raise ValueError(
                    f"Conversation '{conversation.conversation_id}' already exists."
                )
            self._conversations[conversation.conversation_id] = conversation

    async def save(self, conversation: Conversation) -> None:
        with self._lock:
            self._conversations[conversation.conversation_id] = conversation

    async def get(self, conversation_id: str) -> Conversation | None:
        with self._lock:
            return self._conversations.get(conversation_id)

    async def delete(self, conversation_id: str) -> bool:
        with self._lock:
            return self._conversations.pop(conversation_id, None) is not None

    async def exists(self, conversation_id: str) -> bool:
        with self._lock:
            return conversation_id in self._conversations

    async def list(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Conversation]:
        with self._lock:
            items = list(self._conversations.values())
            return items[offset : offset + limit]

    async def count(self) -> int:
        with self._lock:
            return len(self._conversations)

    async def clear(self) -> None:
        with self._lock:
            self._conversations.clear()