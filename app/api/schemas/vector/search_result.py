from pydantic import BaseModel


class SearchResult(BaseModel):
    """
    Search result.
    """

    document_id: str

    text: str

    metadata: dict[str, str]

    score: float