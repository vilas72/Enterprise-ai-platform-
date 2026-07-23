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
from datetime import datetime

from app.gateway.registry import GatewayRegistry
from app.gateway.router import GatewayRouter
from app.workflow.workflow_service import WorkflowService
from app.events.event_publisher import EventPublisher

import logging

from typing import Any

from app.gateway.exceptions import (
    GatewayExecutionError,
)
from app.gateway.models import (
    GatewayExecutionMetadata,
    GatewayExecutionMode,
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
        workflow_service: WorkflowService,        
        publisher: EventPublisher,
        registry: GatewayRegistry,
    ) -> None:

        self._workflow_service = workflow_service
        self._publisher = publisher
        self._registry = registry

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

        await self._publish_started(request)

        metadata = GatewayExecutionMetadata(
            execution_mode=request.execution_mode,
            governance_approved=False,
        )

        try:
            #
            # Validation
            #
            self._validate_request(request)

            #
            # Governance
            #
            await self._authorize(metadata)

            #
            # Execute Workflow
            #
            workflow_result = await self._workflow_service.execute(
                request=request,
            )

            metadata = GatewayExecutionMetadata.from_workflow(
                workflow_result=workflow_result,
                execution_mode=GatewayExecutionMode.WORKFLOW,
                selected_agent=getattr(
                    workflow_result,
                    "selected_agent",
                    None,
                ),
            )

            logger.info(
                "Gateway execution completed.",
                extra={
                    "workflow_id": workflow_result.workflow_id,
                    "execution_id": workflow_result.execution_id,
                    "capability": workflow_result.requested_capability,
                    "agent": workflow_result.selected_agent,
                    "execution_time_ms": workflow_result.execution_time_ms,
                },
            )

            await self._publish_completed(
                request,
                workflow_result,
            )

            return GatewayResponse.from_workflow(
                workflow_result,
                metadata,
            )

        except Exception as exc:

            logger.exception("Gateway execution failed.")

            await self._publish_failed(
                request,
                exc,
            )

            raise GatewayExecutionError(
                message="Workflow execution failed.",
                cause=exc,
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
        return self._registry.agent_names()
    
    def supported_capabilities(
        self,
    ) -> dict[str, list[str]]:
        """
        Return capabilities grouped by agent.
        """
        
        return self._registry.supported_capabilities()

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
    
    async def _publish_started(
        self,
        request: GatewayRequest,
    ) -> None:  
        """
        Publish gateway started event.
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
        
    async def _publish_completed(
        self,
        request: GatewayRequest,
        workflow_result,
    ) -> None:
        """
        Publish gateway completed event.
        """

        await self._publisher.publish(
            Event(
                event_type=EventType.GATEWAY_COMPLETED,
                metadata=EventMetadata(
                    workflow_id=workflow_result.workflow_id,
                    execution_id=workflow_result.execution_id,
                    correlation_id=request.correlation_id or request.request_id,
                    capability=workflow_result.requested_capability,
                    agent=workflow_result.selected_agent,
                    source="EnterpriseGateway",
                ),
                payload={
                    "success": workflow_result.success,
                    "selected_agent": workflow_result.selected_agent,
                    "capability": workflow_result.requested_capability,
                    "execution_time_ms": workflow_result.execution_time_ms,
                },
            )
        )
        
    async def _publish_failed(
        self,
        request: GatewayRequest,
        exc: Exception,
    ) -> None:  
        """
        Publish gateway failed event.
        """

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