from pydantic import BaseModel, Field


class PromptContext(BaseModel):
    """
    Represents prompt template information.
    """

    name: str = Field(
        ...,
        description="Prompt template name",
    )

    variables: dict[str, str] = Field(
        default_factory=dict,
        description="Variables used during rendering",
    )