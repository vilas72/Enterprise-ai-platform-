from pydantic import BaseModel, Field


class PromptContextApi(BaseModel):
    """
    Prompt template information.
    """

    name: str = Field(
        ...,
        description="Prompt template name",
    )

    variables: dict[str, str] = Field(
        default_factory=dict,
        description="Variables used during rendering",
    )