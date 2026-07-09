from __future__ import annotations

from app.conversation.conversation import Conversation
from app.conversation.conversation_message import MessageRole
from app.conversation.conversation_request import ConversationRequest
from app.domain.generate_request import GenerateRequest
from app.domain.models.chat_message import ChatMessage


class GenerateRequestBuilder:
    """
    Responsible for constructing a GenerateRequest from
    conversation state.

    Future responsibilities:
    - Conversation History
    - System Prompt
    - Memory
    - RAG Context
    - Tool Results
    - Guardrails
    """

    def build(
        self,
        conversation: Conversation,
        request: ConversationRequest,
    ) -> GenerateRequest:
        """
        Build a GenerateRequest from the current conversation.
        """

        messages: list[ChatMessage] = []

        self._add_system_prompt(
            messages,
            request,
        )

        self._add_conversation_history(
            messages,
            conversation,
        )

        # Future Extensions
        #
        # self._add_memory(...)
        # self._add_rag_context(...)
        # self._add_tool_results(...)
        #

        return GenerateRequest(
            provider=request.provider,
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens or 1024,
        )

    def _add_system_prompt(
        self,
        messages: list[ChatMessage],
        request: ConversationRequest,
    ) -> None:
        """
        Add an optional system prompt.
        """

        if not request.system_prompt:
            return

        messages.append(
            ChatMessage(
                role=MessageRole.SYSTEM.value,
                content=request.system_prompt,
            )
        )

    def _add_conversation_history(
        self,
        messages: list[ChatMessage],
        conversation: Conversation,
    ) -> None:
        """
        Append the entire conversation history.
        """

        for message in conversation.get_messages():

            messages.append(
                ChatMessage(
                    role=message.role.value,
                    content=message.content,
                )
            )