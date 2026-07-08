"""RAG request model."""

from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    question: str = Field(..., description="User question for retrieval augmented generation.")
    top_k: int | None = Field(default=5, description="Number of context chunks to retrieve.")
    model: str | None = Field(default=None, description="Optional model to use for generation.")
    provider: str | None = Field(default=None, description="Optional provider to use for embedding generation.")
