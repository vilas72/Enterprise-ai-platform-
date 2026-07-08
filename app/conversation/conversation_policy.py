from pydantic import BaseModel, Field


class ConversationPolicy(BaseModel):
    """
    Configuration for conversation memory.
    """

    max_messages: int = Field(
        default=20,
        ge=2,
        description="Maximum messages to keep in memory.",
    )

    preserve_system_messages: bool = Field(
        default=True,
        description="Always keep system messages.",
    )

    preserve_last_messages: int = Field(
        default=10,
        ge=2,
        description="Minimum recent messages to preserve.",
    )

    enable_auto_trim: bool = Field(
        default=True,
        description="Automatically trim old messages.",
    )