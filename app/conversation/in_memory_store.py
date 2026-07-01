from threading import RLock

from app.conversation.conversation_store import ConversationStore
from app.conversation.session import ConversationSession


class InMemoryConversationStore(ConversationStore):
    """
    Thread-safe in-memory conversation store.
    """

    def __init__(self):
        self._sessions: dict[str, ConversationSession] = {}
        self._lock = RLock()

    def create(self) -> ConversationSession:
        session = ConversationSession()

        with self._lock:
            self._sessions[session.session_id] = session

        return session

    def get(
        self,
        session_id: str,
    ) -> ConversationSession | None:

        with self._lock:
            return self._sessions.get(session_id)

    def save(
        self,
        session: ConversationSession,
    ) -> None:

        with self._lock:
            self._sessions[session.session_id] = session

    def delete(
        self,
        session_id: str,
    ) -> None:

        with self._lock:
            self._sessions.pop(session_id, None)

    def exists(
        self,
        session_id: str,
    ) -> bool:

        with self._lock:
            return session_id in self._sessions

    def clear(self) -> None:

        with self._lock:
            self._sessions.clear()

    def count(self) -> int:

        with self._lock:
            return len(self._sessions)