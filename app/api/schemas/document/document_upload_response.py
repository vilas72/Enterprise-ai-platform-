from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):

    success: bool

    filename: str

    chunks: int