from threading import RLock

from app.conversation.conversation import Conversation
from app.conversation.conversation_store import ConversationStore


class InMemoryConversationStore(ConversationStore):
    """
    Thread-safe in-memory conversation store.
    """

    def __init__(self):
        self._conversations: dict[str, Conversation] = {}
        self._lock = RLock()

    async def create(self, conversation: Conversation) -> None:
        with self._lock:
            self._conversations[conversation.conversation_id] = conversation

    async def get(self, conversation_id: str) -> Conversation | None:
        with self._lock:
            return self._conversations.get(conversation_id)

    async def save(self, conversation: Conversation) -> None:
        with self._lock:
            self._conversations[conversation.conversation_id] = conversation

    async def delete(self, conversation_id: str) -> None:
        with self._lock:
            self._conversations.pop(conversation_id, None)

    async def exists(self, conversation_id: str) -> bool:
        with self._lock:
            return conversation_id in self._conversations

    async def clear(self) -> None:
        with self._lock:
            self._conversations.clear()

    async def count(self) -> int:
        with self._lock:
            return len(self._conversations)

    async def list(self, *, limit: int = 100, offset: int = 0) -> list[Conversation]:
        with self._lock:
            conversations = list(self._conversations.values())
            return conversations[offset : offset + limit]