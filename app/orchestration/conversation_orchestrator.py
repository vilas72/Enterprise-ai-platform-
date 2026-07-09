from __future__ import annotations

import logging
import time

from app.conversation.conversation_message import MessageRole
from app.conversation.conversation_request import ConversationRequest
from app.conversation.conversation_response import (
    ConversationResponse,
)
from app.conversation.conversation_service import ConversationService
from app.mappers.conversation_mapper import ConversationMapper
from app.prompt.generate_request_builder import (
    GenerateRequestBuilder,
)
from app.services.ai_service import AIService


logger = logging.getLogger(__name__)


class ConversationOrchestrator:
    """
    Enterprise Conversation Orchestrator.

    Responsible for orchestrating the end-to-end
    conversation lifecycle.

    Responsibilities
    ----------------
    - Validate request
    - Create/Get conversation
    - Persist user message
    - Build AI request
    - Invoke AI Service
    - Persist assistant response
    - Return ConversationResponse

    Future Extensions
    -----------------
    - Memory Manager
    - RAG
    - Tool Calling
    - Agent Framework
    - LangGraph
    - MCP
    - Workflow Engine
    """

    def __init__(
        self,
        conversation_service: ConversationService,
        ai_service: AIService,
        request_builder: GenerateRequestBuilder,
        conversation_mapper: ConversationMapper,
    ) -> None:

        self._conversation_service = conversation_service
        self._ai_service = ai_service
        self._request_builder = request_builder
        self._conversation_mapper = conversation_mapper

    async def process(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Process a complete conversation request.
        """

        request.validate()

        logger.info(
            "Processing conversation '%s'",
            request.conversation_id,
        )

        start_time = time.perf_counter()

        conversation = (
            await self._conversation_service
            .get_or_create_conversation(
                request.conversation_id
            )
        )

        await self._conversation_service.add_message(
            conversation_id=request.conversation_id,
            role=MessageRole.USER,
            content=request.message,
            metadata=request.metadata,
        )

        # Reload conversation so the newly added
        # message becomes part of the history.
        conversation = (
            await self._conversation_service
            .get_conversation(
                request.conversation_id
            )
        )

        generate_request = (
            self._request_builder.build(
                conversation,
                request,
            )
        )

        logger.debug(
            "GenerateRequest created successfully."
        )
        
        try:
            logger.info(
                "Invoking AI provider '%s' using model '%s'.",
                request.provider,
                request.model,
            )

            generate_response = self._ai_service.generate(
                generate_request
            )

        except Exception as ex:
            logger.exception(
                "AI generation failed."
            )

            raise RuntimeError(
                "Failed to generate AI response."
            ) from ex

        logger.debug(
            "AI generation completed successfully."
        )

        assistant_message = (
            await self._conversation_service.add_message(
                conversation_id=request.conversation_id,
                role=MessageRole.ASSISTANT,
                content=generate_response.response,
                token_count=generate_response.total_tokens,
                model=generate_response.model,
            )
        )

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000.0

        logger.info(
            "Conversation '%s' completed in %.2f ms.",
            request.conversation_id,
            elapsed_ms,
        )

        response = (
            self._conversation_mapper
            .to_conversation_response(
                request_id=request.request_id,
                conversation_id=request.conversation_id,
                assistant_message=assistant_message,
                provider=request.provider,
                model=request.model,
                response=generate_response,
                streamed=request.stream,
                latency_ms=elapsed_ms,
            )
        )

        logger.debug(
            "ConversationResponse created successfully."
        )

        return response
    
    async def process_with_memory(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Future entry point for memory-enabled conversations.

        Currently delegates to the standard processing pipeline.
        """

        logger.debug(
            "Memory pipeline not enabled. Falling back to "
            "standard conversation processing."
        )

        return await self.process(request)

    async def process_with_rag(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Future entry point for conversation-aware RAG.

        Currently delegates to the standard processing pipeline.
        """

        logger.debug(
            "RAG pipeline not enabled. Falling back to "
            "standard conversation processing."
        )

        return await self.process(request)

    async def process_with_tools(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Future entry point for Tool Calling.

        Currently delegates to the standard processing pipeline.
        """

        logger.debug(
            "Tool execution pipeline not enabled. "
            "Falling back to standard processing."
        )

        return await self.process(request)

    async def process_agent(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Future entry point for Agent Framework.

        This method will later orchestrate:

        - Planner
        - Memory
        - Tool Selection
        - Tool Execution
        - Reflection
        - Final Response

        For Phase 1 it delegates to the standard pipeline.
        """

        logger.debug(
            "Agent pipeline not enabled."
        )

        return await self.process(request)

    async def process_workflow(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Future entry point for Workflow Engine.

        For Phase 1 it delegates to the
        standard conversation pipeline.
        """

        logger.debug(
            "Workflow pipeline not enabled."
        )

        return await self.process(request)

    async def process_mcp(
        self,
        request: ConversationRequest,
    ) -> ConversationResponse:
        """
        Future entry point for MCP.

        For Phase 1 it delegates to the
        standard conversation pipeline.
        """

        logger.debug(
            "MCP pipeline not enabled."
        )

        return await self.process(request)

    async def health(self) -> dict[str, str]:
        """
        Health information for the orchestrator.

        Returns
        -------
        dict
            Health status.
        """

        return {
            "status": "UP",
            "service": "ConversationOrchestrator",
        }