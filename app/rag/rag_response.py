from pydantic import BaseModel

from app.rag.retrieved_document import RetrievedDocument


class RagResponse(BaseModel):
    """
    RAG response.
    """

    answer: str

    sources: list[RetrievedDocument]