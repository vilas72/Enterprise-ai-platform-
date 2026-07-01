from pydantic import BaseModel, Field


class ChatMessageApi(BaseModel):
    """
    API model representing a chat message.
    """

    role: str = Field(
        ...,
        description="Role of the message sender.",
        examples=["system", "user", "assistant"],
    )

    content: str = Field(
        ...,
        description="Content of the message.",
    )