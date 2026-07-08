from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """
    One chunk of a document.
    """

    id: str

    document_id: str

    chunk_number: int

    text: str

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )