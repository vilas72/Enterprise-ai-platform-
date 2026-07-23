"""
Enterprise Support Agent.

Business orchestration layer responsible for support capabilities.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from app.agents.support.models import (
    SupportAgentRequest,
    SupportAgentResponse,
    SupportCapability,
    SupportExecutionMetadata,
)
from app.agents.support.support_actions import SupportActions

logger = logging.getLogger(__name__)

AsyncHandler = Callable[
    [SupportAgentRequest],
    Awaitable[Any],
]


class SupportAgent:
    """
    Enterprise Support Agent.

    This class contains orchestration only.
    """

    def __init__(
        self,
        support_actions: SupportActions,
    ) -> None:

        self._support = support_actions

        self._handlers: dict[
            SupportCapability,
            AsyncHandler,
        ] = {

            SupportCapability.SEARCH_TICKETS:
                self._support.search_tickets,

            SupportCapability.CREATE_TICKET:
                self._support.create_ticket,

            SupportCapability.UPDATE_TICKET:
                self._support.update_ticket,

            SupportCapability.TRANSITION_TICKET:
                self._support.transition_ticket,

            SupportCapability.SEARCH_KNOWLEDGE:
                self._support.search_knowledge,

            SupportCapability.RECOMMEND_ARTICLES:
                self._support.recommend_articles,

            SupportCapability.SIMILAR_INCIDENTS:
                self._support.similar_incidents,

            SupportCapability.SUMMARIZE_INCIDENT:
                self._support.summarize_incident,

            SupportCapability.GENERATE_RESOLUTION:
                self._support.generate_resolution,

            SupportCapability.ESCALATION_RECOMMENDATION:
                self._support.escalation_recommendation,
                
        }

    async def execute(
        self,
        request: SupportAgentRequest,
    ) -> SupportAgentResponse:

        logger.info(
            "Executing support capability '%s'",
             request.capability.value,
        )

        metadata = SupportExecutionMetadata()

        await self._authorize(
            request,
            metadata,
        )

        try:

            handler = self._handlers.get(
                request.capability
            )

            if handler is None:

                raise ValueError(
                    f"Unsupported capability: "
                    f"{request.capability}"
                )

            handler = self._handlers.get(request.capability)

            if handler is None:
                raise ValueError(
                    f"Unsupported capability: {request.capability}"
                )

            result = await handler(request)
            logger.info("Handler result: %s", result)
            return SupportAgentResponse(
                success=True,
                capability=request.capability,
                message="Support capability executed successfully.",
                result=result,
                metadata=metadata,
            )

        except Exception as exc:

            logger.exception(
                "Support capability failed."
            )

            return SupportAgentResponse(
                success=False,
                capability=request.capability,
                message=str(exc),
                result=None,
                metadata=metadata,
            )

    async def _authorize(
        self,
        request: SupportAgentRequest,
        metadata: SupportExecutionMetadata,
    ) -> None:

        metadata.governance_approved = True

    @property
    def supported_capabilities(
        self,
    ) -> tuple[SupportCapability, ...]:

        return tuple(self._handlers.keys())

    def supports(
        self,
        capability: SupportCapability | str,
    ) -> bool:
        if isinstance(capability, str):
            try:
                capability = SupportCapability(capability)
            except ValueError:
                return False

        return capability in self._handlers

    @property
    def name(self) -> str:
        return "support"

    @property
    def description(self) -> str:
        return "Enterprise Support Agent for ticket operations, incident handling, and support automation."

    def capabilities(self) -> list[str]:
        return [capability.value for capability in self.supported_capabilities]