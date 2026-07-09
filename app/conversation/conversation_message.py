from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class MessageRole(str, Enum):
    """
    Supported conversation roles.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass(slots=True)
class ConversationMessage:
    """
    Represents a single message within a conversation.

    This entity is storage-agnostic and provider-agnostic.
    """

    conversation_id: str
    role: MessageRole
    content: str

    message_id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict[str, Any] = field(default_factory=dict)

    token_count: int | None = None

    model: str | None = None

    def is_user(self) -> bool:
        return self.role == MessageRole.USER

    def is_assistant(self) -> bool:
        return self.role == MessageRole.ASSISTANT

    def is_system(self) -> bool:
        return self.role == MessageRole.SYSTEM

    def is_tool(self) -> bool:
        return self.role == MessageRole.TOOL

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize message.
        """

        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "role": self.role.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "token_count": self.token_count,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConversationMessage":
        """
        Deserialize message.
        """

        return cls(
            message_id=data["message_id"],
            conversation_id=data["conversation_id"],
            role=MessageRole(data["role"]),
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {}),
            token_count=data.get("token_count"),
            model=data.get("model"),
        )