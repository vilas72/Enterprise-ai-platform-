from app.conversation.conversation import Conversation
from app.conversation.conversation_store import ConversationStore
from app.conversation.session import ConversationSession
from app.conversation.conversation_message import MessageRole, ConversationMessage
from app.conversation.conversation_memory_manager import ConversationMemoryManager

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
        memory_manager: ConversationMemoryManager,
    ):
        self._store = conversation_store
        self._memory_manager = memory_manager

    async def create_session(self) -> Conversation:
        """
        Create a new conversation session.
        """
        conversation = Conversation()
        await self._store.save(conversation)
        return conversation

    async def get_session(
        self,
        session_id: str,
    ) -> Conversation | None:
        """
        Retrieve an existing session.
        """
        return await self._store.get(session_id)

    async def save_session(
        self,
        session: Conversation,
    ) -> None:
        """
        Persist a conversation session.
        """
        await self._store.save(session)

    async def delete_session(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a conversation session.
        """
        await self._store.delete(session_id)

    async def add_user_message(
        self,
        session: Conversation,
        message: str,
    ) -> None:
        """
        Append a user message.
        """
        session.add_message(
            role=MessageRole.USER,
            content=message,
        )
        
        #
        # Apply conversation memory policy
        #
        self._memory_manager.apply(session)

        await self.save_session(session)
        

    async def add_assistant_message(
        self,
        session: Conversation,
        message: str,
    ) -> None:
        """
        Append an assistant response.
        """
        session.add_message(
            role=MessageRole.ASSISTANT,
            content=message,
        )

        self._memory_manager.apply(session)
        
        await self.save_session(session)

    def get_messages(
        self,
        session: Conversation,
    ) -> list[ConversationMessage]:
        """
        Return conversation history.
        """
        return session.messages.copy()