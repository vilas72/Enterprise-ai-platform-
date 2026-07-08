from pydantic import BaseModel, Field


class RetrievedDocument(BaseModel):
    """
    Document retrieved from vector search.
    """

    id: str = Field(
        ...,
        description="Document identifier.",
    )

    text: str = Field(
        ...,
        description="Retrieved text.",
    )

    score: float = Field(
        ...,
        description="Similarity score.",
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )