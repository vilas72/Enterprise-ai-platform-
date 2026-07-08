from pydantic import BaseModel, Field


class VectorDocument(BaseModel):
    """
    Represents a document stored in the vector store.
    """

    id: str = Field(
        ...,
        description="Unique document identifier.",
    )

    text: str = Field(
        ...,
        description="Original document text.",
    )

    embedding: list[float] = Field(
        ...,
        description="Embedding vector.",
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Optional document metadata.",
    )