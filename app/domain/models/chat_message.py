from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """
    Represents a single conversation message.
    """

    role: str = Field(
        ...,
        description="Role of the speaker.",
        examples=["system", "user", "assistant"],
    )

    content: str = Field(
        ...,
        description="Message content.",
    )