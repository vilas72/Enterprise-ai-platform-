from pydantic import BaseModel


class IndexResponse(BaseModel):
    """
    Response after indexing.
    """

    document_id: str

    message: str