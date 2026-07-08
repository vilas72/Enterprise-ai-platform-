from pydantic import BaseModel


class EmbeddingResponseApi(BaseModel):
    """
    Embedding API response.
    """

    provider: str

    model: str

    dimensions: int

    embedding: list[float]