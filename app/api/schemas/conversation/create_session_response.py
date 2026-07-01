from pydantic import BaseModel, Field


class CreateSessionResponse(BaseModel):
    """
    Response returned after creating a conversation.
    """

    session_id: str = Field(
        ...,
        description="Conversation session identifier",
    )