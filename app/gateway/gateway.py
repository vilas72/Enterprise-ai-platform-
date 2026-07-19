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
from app.gateway.router import GatewayRouter
from app.workflow.workflow_builder import WorkflowBuilder
from app.workflow.workflow_engine import WorkflowEngine

import logging

from typing import Any

from app.events.event_publisher import EventPublisher

from app.agents.planner.planner import Planner
from app.gateway.exceptions import (
    GatewayExecutionError,
)
from app.gateway.models import (
    GatewayExecutionMetadata,
    GatewayRequest,
    GatewayResponse,
)

from app.events.models.event import Event
from app.events.models.event_metadata import EventMetadata
from app.events.models.event_type import EventType

logger = logging.getLogger(__name__)


class EnterpriseGateway:
    """
    Enterprise Agent Gateway.

    Orchestrates execution of registered business agents.
    """

    def __init__(
        self,
        planner: Planner,
        router: GatewayRouter,
        workflow_builder: WorkflowBuilder,
        workflow_engine: WorkflowEngine,
        publisher: EventPublisher,
    ) -> None:

        self._planner = planner
        self._router = router
        self._workflow_builder = workflow_builder
        self._workflow_engine = workflow_engine
        self._publisher = publisher

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
        
        await self._publisher.publish(
            Event(
                event_type=EventType.GATEWAY_STARTED,
                metadata=EventMetadata(
                    correlation_id = request.correlation_id or request.request_id,
                    source="EnterpriseGateway",
                ),
                payload={
                    "capability": request.capability,
                    "execution_mode": request.execution_mode.value,
                    "user_id": request.user_id,
                }
            )
        )

        metadata = GatewayExecutionMetadata(
            execution_mode=request.execution_mode,
        )

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
            # Planning
            #

            plan = await self._planner.plan(request)

            metadata.selected_agent = plan.selected_agent

            logger.info(
                "Planner selected '%s' for '%s'",
                plan.selected_agent,
                plan.capability,
            )

            #
            # Build Workflow
            #

            workflow = self._workflow_builder.build(
                plan,
            )

            #
            # Execute Workflow
            #

            workflow_result = await self._workflow_engine.execute(
                workflow=workflow,
                request=request,
            )

            #
            # Populate Gateway Metadata
            #

            metadata.execution_started_at = workflow_result.started_at
            metadata.execution_completed_at = workflow_result.completed_at
            metadata.execution_time_ms = workflow_result.execution_time_ms

            logger.info(
                "Gateway execution completed in %.2f ms.",
                workflow_result.execution_time_ms,
            )

            await self._publisher.publish(
                Event(
                    event_type=EventType.GATEWAY_COMPLETED,
                    metadata=EventMetadata(
                        workflow_id=workflow.id,
                        execution_id=workflow_result.execution_id,
                        correlation_id = request.correlation_id or request.request_id,
                        source="EnterpriseGateway",
                    ),
                    payload={
                        "success": workflow_result.success,
                        "selected_agent": plan.selected_agent,
                        "capability": plan.capability,
                        "execution_time_ms": workflow_result.execution_time_ms,
                    }
                )
            )
            return GatewayResponse(
                success=workflow_result.success,
                message=(
                    "Execution completed successfully."
                    if workflow_result.success
                    else workflow_result.error or "Execution failed."
                ),
                result=workflow_result.result,
                metadata=metadata,
            )

        except Exception as exc:

            logger.exception(
                "Gateway execution failed."
            )
            await self._publisher.publish(
                Event(
                    event_type=EventType.GATEWAY_FAILED,
                    metadata=EventMetadata(
                        correlation_id = request.correlation_id or request.request_id,
                        source="EnterpriseGateway",
                    ),
                    payload={
                        "success": False,
                        "capability": request.capability,
                        "error": str(exc),
                    },
                )
            )
            raise GatewayExecutionError(
                f"Workflow execution failed: {exc}",
            ) from exc
        
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