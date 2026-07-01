from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    """
    Represents metadata about an AI model supported
    by the Enterprise AI Platform.
    """

    provider: str = Field(
        ...,
        description="AI provider name",
        examples=["openai", "gemini"],
    )

    name: str = Field(
        ...,
        description="Internal model identifier",
        examples=["gpt-4.1", "gemini-2.5-pro"],
    )

    display_name: str = Field(
        ...,
        description="Human-readable model name",
        examples=["GPT-4.1", "Gemini 2.5 Pro"],
    )

    default: bool = Field(
        default=False,
        description="Whether this is the default model for the provider",
    )

    supports_streaming: bool = Field(
        default=False,
        description="Whether the model supports streaming responses",
    )