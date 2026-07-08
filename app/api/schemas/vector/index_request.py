from pydantic import BaseModel, Field


class IndexRequest(BaseModel):
    """
    Request for indexing a document.
    """

    document_id: str | None = Field(
        default=None,
        description="Optional document id.",
    )

    text: str = Field(
        ...,
        description="Document text.",
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Document metadata.",
    )

    provider: str | None = None

    model: str | None = None