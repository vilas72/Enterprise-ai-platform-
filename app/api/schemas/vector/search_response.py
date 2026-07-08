from pydantic import BaseModel

from app.api.schemas.vector.search_result import SearchResult


class SearchResponse(BaseModel):
    """
    Search response.
    """

    total: int

    results: list[SearchResult]