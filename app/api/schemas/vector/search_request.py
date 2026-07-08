from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """
    Vector search request.
    """

    query: str = Field(
        ...,
        description="Search query.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    provider: str | None = None

    model: str | None = None