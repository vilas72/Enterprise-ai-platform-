from pydantic import BaseModel


class SourceApi(BaseModel):
    """
    Source document returned by RAG.
    """

    id: str

    score: float

    text: str

    metadata: dict[str, str]