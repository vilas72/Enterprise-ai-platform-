from typing import List

from pydantic import BaseModel, Field, model_validator

from app.api.schemas.chat_message_api import ChatMessageApi

from app.api.schemas.prompt_context_api import PromptContextApi


class GenerateRequestApi(BaseModel):
    """
    API request model for AI generation.

    Supports both:
    - Legacy prompt-based requests
    - Conversation/message-based requests
    """

    provider: str | None = Field(
        default=None,
        description="AI provider",
        examples=["openai", "gemini"],
    )

    model: str | None = Field(
        default=None,
        description="Optional model name",
        examples=["gpt-4.1", "gemini-2.5-pro"],
    )

    prompt: str | None = Field(
        default=None,
        description="Legacy prompt",
        examples=["Explain SOLID principles"],
    )

    messages: List[ChatMessageApi] = Field(
        default_factory=list,
        description="Conversation messages",
    )

    system_prompt: str | None = Field(
        default=None,
        description="Optional system prompt",
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=1024,
        gt=0,
    )
    
    prompt_context: PromptContextApi | None = None
    
    @model_validator(mode="after")
    def validate_request(self):
        """
        Ensure at least one input is provided.
        """

        if not self.prompt and not self.messages:
            raise ValueError(
                "Either 'prompt' or 'messages' must be provided."
            )

        return self