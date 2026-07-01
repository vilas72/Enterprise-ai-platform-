from pydantic import BaseModel


class ModelResponse(BaseModel):
    """
    Represents an AI model exposed by the platform.
    """

    provider: str

    name: str

    display_name: str

    default: bool

    supports_streaming: bool