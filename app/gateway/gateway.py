"""
Enterprise Gateway.

The Enterprise Gateway is the unified entry point for all
business agents. It is responsible for:

- Request validation
- Governance orchestration
- Agent routing
- Agent execution
- Response orchestration

The gateway intentionally contains no business logic.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from app.gateway.exceptions import (
    GatewayExecutionError,
)
from app.gateway.models import (
    GatewayExecutionMetadata,
    GatewayRequest,
    GatewayResponse,
)
from app.gateway.router import GatewayRouter

logger = logging.getLogger(__name__)


class EnterpriseGateway:
    """
    Enterprise Agent Gateway.

    Orchestrates execution of registered business agents.
    """

    def __init__(
        self,
        router: GatewayRouter,
    ) -> None:

        self._router = router

    # ==========================================================
    # Public API
    # ==========================================================

    async def execute(
        self,
        request: GatewayRequest,
    ) -> GatewayResponse:
        """
        Execute an enterprise request.
        """

        logger.info(
            "Gateway received capability '%s'.",
            request.capability,
        )

        metadata = GatewayExecutionMetadata(
            execution_mode=request.execution_mode,
        )

        started = datetime.utcnow()

        try:

            #
            # Validation
            #

            self._validate_request(request)

            #
            # Governance
            #

            await self._authorize(
                request,
                metadata,
            )

            #
            # Route
            #

            agent = await self._router.route(
                request,
            )

            metadata.selected_agent = (
                agent.__class__.__name__
            )

            #
            # Execute
            #
            
            agent_request = self._router.build_agent_request(
                agent=agent,
                request=request,
            )
            
            logger.info(
                "Agent request type: %s",
                type(agent_request),
            )

            result = await self._execute_agent(
                agent=agent,
                request=agent_request,
            )
            #
            # Metrics
            #

            completed = datetime.utcnow()

            metadata.execution_completed_at = (
                completed
            )

            metadata.execution_time_ms = (
                completed - started
            ).total_seconds() * 1000

            logger.info(
                "Gateway execution completed."
            )

            return GatewayResponse(
                success=True,
                message="Execution completed successfully.",
                result=result,
                metadata=metadata,
            )

        except Exception as exc:

            completed = datetime.utcnow()

            metadata.execution_completed_at = (
                completed
            )

            metadata.execution_time_ms = (
                completed - started
            ).total_seconds() * 1000

            logger.exception(
                "Gateway execution failed."
            )

            raise GatewayExecutionError(
                str(exc),
            ) from exc

    # ==========================================================
    # Agent Execution
    # ==========================================================

    async def _execute_agent(
        self,
        *,
        agent: Any,
        request: Any,
    ) -> Any:
        return await agent.execute(request)
    # ==========================================================
    # Validation
    # ==========================================================

    @staticmethod
    def _validate_request(
        request: GatewayRequest,
    ) -> None:
        """
        Validate gateway request.
        """

        if not request.capability:

            raise ValueError(
                "Capability is required."
            )

    # ==========================================================
    # Governance
    # ==========================================================

    async def _authorize(
        self,
        request: GatewayRequest,
        metadata: GatewayExecutionMetadata,
    ) -> None:
        """
        Governance hook.

        This method will later integrate with the
        Governance Runtime.
        """

        metadata.governance_approved = True

        logger.debug(
            "Governance approved."
        )
        
        # ==========================================================
    # Multi-Agent Execution
    # ==========================================================

    async def execute_many(
        self,
        requests: list[GatewayRequest],
    ) -> list[GatewayResponse]:
        """
        Execute multiple gateway requests sequentially.

        This method provides the foundation for future
        multi-agent orchestration.
        """

        responses: list[GatewayResponse] = []

        for request in requests:
            responses.append(
                await self.execute(request)
            )

        return responses

    # ==========================================================
    # Gateway Information
    # ==========================================================

    def supported_agents(
        self,
    ) -> list[str]:
        """
        Return registered agent names.
        """

        return self._router.registered_agents()

    def supported_capabilities(
        self,
    ) -> dict[str, list[str]]:
        """
        Return capabilities grouped by agent.
        """

        return self._router.supported_capabilities()

    # ==========================================================
    # Health
    # ==========================================================

    async def health(
        self,
    ) -> dict[str, Any]:
        """
        Gateway health information.
        """

        return {
            "healthy": True,
            "registered_agents": self.supported_agents(),
            "capabilities": self.supported_capabilities(),
        }

    # ==========================================================
    # Future Extension Hooks
    # ==========================================================

    async def execute_workflow(
        self,
        request: GatewayRequest,
    ) -> GatewayResponse:
        """
        Workflow execution hook.

        Future integration:
            - Workflow Runtime
            - Agentic Runtime
            - Multi-Agent Runtime
        """

        logger.info(
            "Workflow execution requested."
        )

        return await self.execute(request)

    async def execute_multi_agent(
        self,
        requests: list[GatewayRequest],
    ) -> list[GatewayResponse]:
        """
        Multi-agent execution hook.

        Future integration:
            - Multi-Agent Coordinator
            - Task Dispatcher
            - Result Aggregator
        """

        logger.info(
            "Multi-agent execution requested."
        )

        return await self.execute_many(requests)