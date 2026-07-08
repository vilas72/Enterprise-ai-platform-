from pydantic import BaseModel


class PromptResponse(BaseModel):
    """
    Prompt template response.
    """

    name: str

    content: str