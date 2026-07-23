"""
Workflow Service.
"""

from __future__ import annotations

from app.gateway.models import GatewayRequest
from app.agents.planner.planner import Planner
from app.workflow.models.workflow_result import WorkflowResult
from app.workflow.workflow_builder import WorkflowBuilder
from app.workflow.workflow_engine import WorkflowEngine
from app.workflow.workflow_registry import WorkflowRegistry


class WorkflowService:
    """
    Orchestrates planning, workflow creation,
    registration and execution.

    This is the public entry point for workflow execution.
    """

    def __init__(
        self,
        planner: Planner,
        builder: WorkflowBuilder,
        registry: WorkflowRegistry,
        engine: WorkflowEngine,
        
    ) -> None:
        self._planner = planner
        self._builder = builder
        self._registry = registry
        self._engine = engine

    async def execute(
        self,
        request: GatewayRequest,
    ) -> WorkflowResult:
        """
        Execute a request through the workflow engine.

        Flow:

        GatewayRequest
            ↓
        Planner
            ↓
        WorkflowBuilder
            ↓
        WorkflowRegistry
            ↓
        WorkflowEngine
        """

        planner_result = await self._planner.plan(request)

        workflow = self._builder.build(planner_result)

        if not self._registry.exists(workflow.id):
            self._registry.register(workflow)

        workflow_result = await self._engine.execute(
            workflow=workflow,
            request=request,
        )

        workflow_result.requested_capability = (
            planner_result.requested_capability
        )

        workflow_result.workflow_capability = (
            planner_result.workflow_capability
        )

        workflow_result.selected_agent = (
            planner_result.selected_agent
        )

        workflow_result.planner = (
            planner_result.planner
        )

        workflow_result.confidence = (
            planner_result.payload.get("confidence")
            if planner_result.payload
            else None
        )

        workflow_result.workflow_version = workflow.version 

        return workflow_result