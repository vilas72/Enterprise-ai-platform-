from pydantic import BaseModel, Field

from app.vectorstore.vector_document import VectorDocument


class VectorSearchResult(BaseModel):
    """
    Represents a similarity search result.
    """

    document: VectorDocument = Field(
        ...,
        description="Matched document.",
    )

    score: float = Field(
        ...,
        description="Similarity score.",
    )