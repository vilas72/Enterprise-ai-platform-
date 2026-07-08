from pydantic import BaseModel

from app.api.schemas.rag.source_api import SourceApi


class RagResponseApi(BaseModel):
    """
    RAG API response.
    """

    answer: str

    sources: list[SourceApi]