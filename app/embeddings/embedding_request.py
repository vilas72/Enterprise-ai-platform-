from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    """
    Request for generating embeddings.
    """

    text: str = Field(
        ...,
        description="Text to generate embedding for.",
    )

    provider: str | None = Field(
        default=None,
        description="Embedding provider.",
    )

    model: str | None = Field(
        default=None,
        description="Embedding model.",
    )