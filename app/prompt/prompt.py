from pydantic import BaseModel, Field


class Prompt(BaseModel):
    """
    Represents a prompt template.
    """

    name: str = Field(
        ...,
        description="Prompt name",
    )

    content: str = Field(
        ...,
        description="Prompt template",
    )