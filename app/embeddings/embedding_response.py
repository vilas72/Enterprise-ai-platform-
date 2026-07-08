from pydantic import BaseModel, Field


class EmbeddingResponse(BaseModel):
    """
    Embedding generation response.
    """

    provider: str

    model: str

    dimensions: int

    embedding: list[float]