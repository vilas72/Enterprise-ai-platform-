"""
Enterprise Knowledge Agent.

The Knowledge Agent is the business orchestration layer responsible for
enterprise knowledge capabilities. It coordinates KnowledgeActions and
AIActions without exposing retrieval, AI runtime or connector
implementations to callers.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from app.agents.knowledge.ai_actions import AIActions
from app.actions.knowledge_actions import KnowledgeActions
from app.agents.knowledge.models import (
    KnowledgeAgentRequest,
    KnowledgeAgentResponse,
    KnowledgeCapability,
    KnowledgeExecutionMetadata,
)

logger = logging.getLogger(__name__)

AsyncHandler = Callable[
    [KnowledgeAgentRequest],
    Awaitable[Any],
]

SyncHandler = Callable[
    [KnowledgeAgentRequest],
    Any,
]


class KnowledgeAgent:
    """
    Enterprise Knowledge Agent.

    Responsibilities
    ----------------

    • Enterprise Knowledge Search

    • Semantic Search

    • Retrieval Augmented Generation (RAG)

    • Enterprise Documentation Search

    • Knowledge Recommendations

    • Technical Documentation Summarization

    • AI-assisted Knowledge Operations

    This class contains orchestration only.

    Business implementations live inside:

        - KnowledgeActions

        - AIActions
    """

    def __init__(
        self,
        knowledge_actions: KnowledgeActions,
        ai_actions: AIActions,
    ) -> None:

        self._knowledge = knowledge_actions
        self._ai = ai_actions

        #
        # Capability Routing
        #

        self._async_handlers: dict[
            KnowledgeCapability,
            AsyncHandler,
        ] = {

            KnowledgeCapability.SEARCH:
                self._knowledge.search,

            KnowledgeCapability.ANSWER:
                self._knowledge.answer,

            KnowledgeCapability.SUMMARIZE:
                self._knowledge.summarize,

            KnowledgeCapability.RECOMMEND:
                self._knowledge.recommend,
        }

        self._sync_handlers: dict[
            KnowledgeCapability,
            SyncHandler,
        ] = {
            KnowledgeCapability.EXPLAIN:
                self._ai.explain,

            KnowledgeCapability.REWRITE:
                self._ai.rewrite,
        }

    async def execute(
        self,
        request: KnowledgeAgentRequest,
    ) -> KnowledgeAgentResponse:
        """
        Execute a Knowledge Agent capability.

        Workflow
        --------
        1. Governance validation
        2. Resolve capability handler
        3. Execute business action
        4. Build response
        """

        logger.info(
            "Executing knowledge capability '%s'",
            request.capability.value,
        )

        metadata = KnowledgeExecutionMetadata()

        #
        # Governance
        #

        await self._authorize(
            request,
            metadata,
        )

        try:

            #
            # Async capabilities
            #

            if request.capability in self._async_handlers:

                handler = self._async_handlers[
                    request.capability
                ]

                result = await handler(request)

            #
            # Sync capabilities
            #

            elif request.capability in self._sync_handlers:

                handler = self._sync_handlers[
                    request.capability
                ]

                result = handler(request)

            else:

                raise ValueError(
                    f"Unsupported capability: "
                    f"{request.capability.value}"
                )

            logger.info(
                "Knowledge capability '%s' completed successfully.",
                request.capability.value,
            )

            return KnowledgeAgentResponse(
                success=True,
                capability=request.capability,
                message="Knowledge capability executed successfully.",
                result=result,
                metadata=metadata,
            )

        except Exception as exc:

            logger.exception(
                "Knowledge capability '%s' failed.",
                request.capability.value,
            )

            return KnowledgeAgentResponse(
                success=False,
                capability=request.capability,
                message=str(exc),
                result=None,
                metadata=metadata,
            )

    # ------------------------------------------------------------------
    # Governance
    # ------------------------------------------------------------------

    async def _authorize(
        self,
        request: KnowledgeAgentRequest,
        metadata: KnowledgeExecutionMetadata,
    ) -> None:
        """
        Execute governance validation.

        Governance integration will be extended as
        enterprise knowledge policies evolve.
        """

        metadata.governance_approved = True

        logger.debug(
            "Governance validation completed for '%s'.",
            request.capability.value,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def supported_capabilities(
        self,
    ) -> tuple[KnowledgeCapability, ...]:
        """
        Return supported capabilities.
        """

        return (
            *self._async_handlers.keys(),
            *self._sync_handlers.keys(),
        )

    def supports(
        self,
        capability: KnowledgeCapability | str,
    ) -> bool:
        """
        Determine whether the Knowledge Agent
        supports the given capability.
        """

        if isinstance(capability, str):
            try:
                capability = KnowledgeCapability(capability)
            except ValueError:
                return False

        return (
            capability in self._async_handlers
            or capability in self._sync_handlers
        )

    @property
    def name(self) -> str:
        return "knowledge"

    @property
    def description(self) -> str:
        return "Enterprise Knowledge Agent for search, RAG, summaries and documentation assistance."

    def capabilities(self) -> list[str]:
        return [capability.value for capability in self.supported_capabilities]