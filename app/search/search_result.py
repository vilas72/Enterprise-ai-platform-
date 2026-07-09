from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """
    Unified search result.
    """

    document_id: str

    text: str

    score: float

    source: str

    metadata: dict[str, str] = Field(default_factory=dict)