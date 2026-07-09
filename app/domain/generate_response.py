from pydantic import BaseModel, Field


class GenerateResponse(BaseModel):
    """
    Represents the normalized response returned by any AI provider.

    This model is provider-agnostic and is used throughout the
    Enterprise AI Platform.
    """

    provider: str

    model: str

    response: str

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    latency_ms: float = 0.0

    finish_reason: str = Field(
        default="stop",
        description="Reason generation finished."
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
        description="Provider specific metadata."
    )