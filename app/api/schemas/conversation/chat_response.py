from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """
    Response returned from a conversation chat.
    """

    session_id: str = Field(...)

    provider: str = Field(...)

    model: str = Field(...)

    response: str = Field(...)