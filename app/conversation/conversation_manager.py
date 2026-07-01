from app.conversation.conversation_store import ConversationStore
from app.conversation.session import ConversationSession
from app.domain.models.chat_message import ChatMessage


class ConversationManager:
    """
    Manages conversation lifecycle.

    Responsible for:
    - Creating sessions
    - Loading sessions
    - Appending messages
    - Persisting conversations
    """

    def __init__(
        self,
        conversation_store: ConversationStore,
    ):
        self._store = conversation_store

    def create_session(self) -> ConversationSession:
        """
        Create a new conversation session.
        """
        return self._store.create()

    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """
        Retrieve an existing session.
        """
        return self._store.get(session_id)

    def save_session(
        self,
        session: ConversationSession,
    ) -> None:
        """
        Persist a conversation session.
        """
        self._store.save(session)

    def delete_session(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a conversation session.
        """
        self._store.delete(session_id)

    def add_user_message(
        self,
        session: ConversationSession,
        message: str,
    ) -> None:
        """
        Append a user message.
        """

        session.add_message(
            ChatMessage(
                role="user",
                content=message,
            )
        )

        self.save_session(session)

    def add_assistant_message(
        self,
        session: ConversationSession,
        message: str,
    ) -> None:
        """
        Append an assistant response.
        """

        session.add_message(
            ChatMessage(
                role="assistant",
                content=message,
            )
        )

        self.save_session(session)

    def get_messages(
        self,
        session: ConversationSession,
    ) -> list[ChatMessage]:
        """
        Return conversation history.
        """

        return session.messages.copy()