from pydantic import BaseModel, Field

from app.api.schemas.chat_message_api import ChatMessageApi


class ConversationResponse(BaseModel):
    """
    Returns the complete conversation.
    """

    session_id: str = Field(...)

    messages: list[ChatMessageApi] = Field(
        default_factory=list
    )