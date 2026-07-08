from fastapi import logger

from app.conversation.conversation_policy import ConversationPolicy
from app.conversation.session import ConversationSession
from app.domain.models.chat_message import ChatMessage


class ConversationMemoryManager:
    """
    Responsible for managing conversation memory.

    Current capabilities:
    - Auto trim

    Future:
    - Summarization
    - Token budgeting
    - Semantic memory
    """

    def __init__(
        self,
        policy: ConversationPolicy | None = None,
    ) -> None:

        self._policy = policy or ConversationPolicy()

    def apply(
        self,
        session: ConversationSession,
    ) -> None:
        """
        Apply memory policy to a conversation session.
        """

        if not self._policy.enable_auto_trim:
            return

        self._trim(session)

    def _trim(
        self,
        session: ConversationSession,
    ) -> None:
        """
        Trim conversation history.
        """

        if len(session.messages) <= self._policy.max_messages:
            return

        system_messages: list[ChatMessage] = []
        regular_messages: list[ChatMessage] = []

        for message in session.messages:

            if (
                self._policy.preserve_system_messages
                and message.role.lower() == "system"
            ):
                system_messages.append(message)
            else:
                regular_messages.append(message)

        keep = regular_messages[
            -self._policy.preserve_last_messages:
        ]

        session.messages = system_messages + keep
        
        logger.info(
        "Conversation trimmed: %s -> %s messages",
        len(regular_messages),
        len(keep),
    )

    @property
    def policy(
        self,
    ) -> ConversationPolicy:
        """
        Return the active conversation policy.
        """

        return self._policy