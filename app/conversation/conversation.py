from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.conversation.conversation_message import (
    ConversationMessage,
    MessageRole,
)


@dataclass(slots=True)
class Conversation:
    """
    Aggregate root representing a conversation.

    A Conversation owns all ConversationMessage entities and
    encapsulates conversation-related business logic.
    """

    conversation_id: str = field(default_factory=lambda: str(uuid4()))

    title: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = field(default_factory=dict)

    messages: list[ConversationMessage] = field(default_factory=list)

    def add_message(
        self,
        role: MessageRole,
        content: str,
        *,
        metadata: dict[str, Any] | None = None,
        token_count: int | None = None,
        model: str | None = None,
    ) -> ConversationMessage:
        """
        Create and append a new message to the conversation.
        """

        message = ConversationMessage(
            conversation_id=self.conversation_id,
            role=role,
            content=content,
            metadata=metadata or {},
            token_count=token_count,
            model=model,
        )

        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)

        return message

    def append_message(
        self,
        message: ConversationMessage,
    ) -> None:
        """
        Append an existing message to the conversation.
        """

        if message.conversation_id != self.conversation_id:
            raise ValueError(
                "Message conversation_id does not match conversation."
            )

        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)

    def get_messages(self) -> list[ConversationMessage]:
        """
        Return all messages.
        """

        return list(self.messages)

    def get_last_message(self) -> ConversationMessage | None:
        """
        Return the latest message.
        """

        if not self.messages:
            return None

        return self.messages[-1]

    def get_messages_by_role(
        self,
        role: MessageRole,
    ) -> list[ConversationMessage]:
        """
        Return all messages matching the given role.
        """

        return [
            message
            for message in self.messages
            if message.role == role
        ]

    def clear_messages(self) -> None:
        """
        Remove all messages from the conversation.
        """

        self.messages.clear()
        self.updated_at = datetime.now(timezone.utc)

    def message_count(self) -> int:
        """
        Return the total number of messages.
        """

        return len(self.messages)

    def is_empty(self) -> bool:
        """
        Return True if the conversation contains no messages.
        """

        return not self.messages

    def rename(self, title: str) -> None:
        """
        Update the conversation title.
        """

        self.title = title
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the conversation.
        """

        return {
            "conversation_id": self.conversation_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
            "messages": [
                message.to_dict()
                for message in self.messages
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Conversation":
        """
        Deserialize a conversation.
        """

        return cls(
            conversation_id=data["conversation_id"],
            title=data.get("title"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            metadata=data.get("metadata", {}),
            messages=[
                ConversationMessage.from_dict(item)
                for item in data.get("messages", [])
            ],
        )