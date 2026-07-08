

from typing import List

from pydantic import BaseModel, Field, model_validator

from app.domain.models.chat_message import ChatMessage

from app.domain.value_objects.prompt_context import PromptContext



class GenerateRequest(BaseModel):
    """
    Domain request for AI generation.

    Supports both:
    - Legacy prompt-based requests
    - Multi-turn conversation requests
    """
    
    provider: str | None = Field(
        default=None,
        description="AI provider name",
    )

    model: str | None = Field(
        default=None,
        description="Model name",
    )

    prompt: str | None = Field(
        default=None,
        description="Legacy prompt",
    )

    messages: List[ChatMessage] = Field(
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
    
    prompt_context: PromptContext | None = None
     
    @model_validator(mode="after")
    def populate_messages(self):
        """
        Backward compatibility.

        If only prompt is supplied,
        automatically create a user message.
        """

        if not self.messages and self.prompt:
            self.messages.append(
                ChatMessage(
                    role="user",
                    content=self.prompt,
                )
            )

        return self