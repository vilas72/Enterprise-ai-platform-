from abc import ABC, abstractmethod

from app.conversation.session import ConversationSession


class ConversationStore(ABC):
    """
    Abstract conversation storage.

    This allows us to swap storage implementations
    without changing business logic.
    """

    @abstractmethod
    def create(self) -> ConversationSession:
        """
        Create a new conversation session.
        """
        pass

    @abstractmethod
    def get(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """
        Retrieve a conversation session.
        """
        pass

    @abstractmethod
    def save(
        self,
        session: ConversationSession,
    ) -> None:
        """
        Persist a conversation session.
        """
        pass

    @abstractmethod
    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a conversation session.
        """
        pass

    @abstractmethod
    def exists(
        self,
        session_id: str,
    ) -> bool:
        """
        Check whether a session exists.
        """
        pass