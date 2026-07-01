from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domain.models.chat_message import ChatMessage


class ConversationSession(BaseModel):
    """
    Represents one conversation session.
    """

    session_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    messages: list[ChatMessage] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    def add_message(
        self,
        message: ChatMessage,
    ) -> None:

        self.messages.append(message)

        self.updated_at = datetime.utcnow()