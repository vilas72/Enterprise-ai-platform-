from pydantic import BaseModel, Field


class EmbeddingRequestApi(BaseModel):
    """
    Embedding API request.
    """

    text: str = Field(
        ...,
        description="Text to embed.",
    )

    provider: str | None = None

    model: str | None = None