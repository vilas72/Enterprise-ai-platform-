from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request within an existing conversation.
    """

    provider: str | None = Field(
        default=None,
        description="AI provider",
    )

    model: str | None = Field(
        default=None,
        description="Model name",
    )

    message: str = Field(
        ...,
        description="User message",
    )

    temperature: float = Field(
        default=0.7,
    )

    max_tokens: int = Field(
        default=1024,
    )