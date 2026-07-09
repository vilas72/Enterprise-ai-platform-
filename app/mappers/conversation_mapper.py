from __future__ import annotations

from app.conversation.conversation import Conversation
from app.conversation.conversation_message import (
    ConversationMessage,
    MessageRole,
)
from app.conversation.conversation_request import ConversationRequest
from app.conversation.conversation_response import (
    ConversationResponse,
    TokenUsage,
)
from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse
from app.domain.models.chat_message import ChatMessage


class ConversationMapper:
    """
    Maps conversation domain objects to AI domain models and back.

    Responsibilities:
    - Conversation -> GenerateRequest
    - ConversationMessage -> ChatMessage
    - GenerateResponse -> ConversationResponse
    """

    @staticmethod
    def to_generate_request(
        conversation: Conversation,
        request: ConversationRequest,
    ) -> GenerateRequest:
        """
        Build a GenerateRequest using the full conversation history.
        """

        messages = [
            ConversationMapper.to_chat_message(message)
            for message in conversation.get_messages()
        ]

        return GenerateRequest(
            provider=request.provider,
            model=request.model,
            messages=messages,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens or 1024,
        )

    @staticmethod
    def to_chat_message(
        message: ConversationMessage,
    ) -> ChatMessage:
        """
        Convert a ConversationMessage into a ChatMessage.
        """

        return ChatMessage(
            role=message.role.value,
            content=message.content,
        )

    @staticmethod
    def to_conversation_response(
        *,
        request_id: str,
        conversation_id: str,
        assistant_message: ConversationMessage,
        provider: str,
        model: str,
        response: GenerateResponse,
        streamed: bool = False,
        latency_ms: float | None = None,
    ) -> ConversationResponse:
        """
        Convert GenerateResponse into ConversationResponse.
        """

        return ConversationResponse(
            request_id=request_id,
            conversation_id=conversation_id,
            message=assistant_message,
            provider=provider,
            model=model,
            usage=TokenUsage(
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                total_tokens=response.total_tokens,
            ),
            finish_reason=response.finish_reason,
            latency_ms=latency_ms,
            streamed=streamed,
        )

    @staticmethod
    def create_assistant_message(
        conversation_id: str,
        response: GenerateResponse,
    ) -> ConversationMessage:
        """
        Create an assistant ConversationMessage from an AI response.
        """

        return ConversationMessage(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=response.response,
            model=response.model,
            token_count=response.total_tokens,
        )