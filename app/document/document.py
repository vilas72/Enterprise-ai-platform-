from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    Raw document loaded from a source.
    """

    id: str = Field(
        ...,
        description="Unique document identifier.",
    )

    name: str = Field(
        ...,
        description="Document name.",
    )

    text: str = Field(
        ...,
        description="Full document content.",
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )