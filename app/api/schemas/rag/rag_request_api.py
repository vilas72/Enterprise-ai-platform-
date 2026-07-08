from pydantic import BaseModel, Field


class RagRequestApi(BaseModel):
    """
    RAG API request.
    """

    question: str = Field(
        ...,
        description="User question.",
    )

    provider: str | None = None

    model: str | None = None

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )