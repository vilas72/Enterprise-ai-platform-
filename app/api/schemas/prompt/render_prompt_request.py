from pydantic import BaseModel, Field


class RenderPromptRequest(BaseModel):
    """
    Request used to render a prompt.
    """

    variables: dict[str, str] = Field(
        default_factory=dict
    )