"""
Workflow Engine.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.events.event_publisher import EventPublisher
from app.events.models.event import Event
from app.events.models.event_metadata import EventMetadata
from app.events.models.event_type import EventType

from app.gateway.models import GatewayRequest

from app.workflow.hooks.workflow_hook_manager import WorkflowHookManager
from app.workflow.models.workflow_context import WorkflowContext
from app.workflow.models.workflow_definition import WorkflowDefinition
from app.workflow.models.workflow_execution import (
    WorkflowExecution,
    WorkflowExecutionStatus,
)
from app.workflow.models.workflow_result import WorkflowResult
from app.workflow.workflow_executor import WorkflowExecutor


class WorkflowEngine:
    """
    Enterprise Workflow Engine.
    """

    def __init__(
        self,
        executor: WorkflowExecutor,
        publisher: EventPublisher,
        hooks: WorkflowHookManager,
    ) -> None:
        self._executor = executor
        self._publisher = publisher
        self._hooks = hooks

    async def execute(
        self,
        workflow: WorkflowDefinition,
        request: GatewayRequest,
    ) -> WorkflowResult:
        """
        Execute a workflow.
        """

        started_at = datetime.now(UTC)
        execution_id = str(uuid.uuid4())

        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow=workflow,
            context=WorkflowContext(
                workflow_id=workflow.id,
                execution_id=execution_id,
                variables=request.payload or {},
                request=request,
            ),
            status=WorkflowExecutionStatus.RUNNING,
            started_at=started_at,
        )

        # Validate workflow
        self._validate_workflow(workflow)
        
        await self._hooks.before_workflow(
            workflow=workflow,
            context=execution.context,
        )

        await self._publisher.publish(
            Event(
                event_type=EventType.WORKFLOW_STARTED,
                metadata=EventMetadata(
                    workflow_id=workflow.id,
                    execution_id=execution.execution_id,
                    source="WorkflowEngine",
                ),
                payload={
                    "workflow_name": workflow.name,
                    "step_count": len(workflow.steps),
                },
            )
        )

        try:

            result = await self._executor.execute(
                workflow=workflow,
                context=execution.context,
            )

            execution.status = (
                WorkflowExecutionStatus.COMPLETED
                if result.success
                else WorkflowExecutionStatus.FAILED
            )

            execution.completed_at = datetime.now(UTC)

            result.started_at = execution.started_at
            result.completed_at = execution.completed_at
            result.execution_time_ms = (
                execution.completed_at - execution.started_at
            ).total_seconds() * 1000
            
            await self._hooks.after_workflow(
                workflow=workflow,
                context=execution.context,
            )

            await self._publisher.publish(
                Event(
                    event_type=EventType.WORKFLOW_COMPLETED,
                    metadata=EventMetadata(
                        workflow_id=workflow.id,
                        execution_id=execution.execution_id,
                        source="WorkflowEngine",
                    ),
                    payload={
                        "success": result.success,
                        "execution_time_ms": result.execution_time_ms,
                    },
                )
            )

            return result

        except Exception as exc:

            execution.status = WorkflowExecutionStatus.FAILED
            execution.completed_at = datetime.now(UTC)
            execution.error = str(exc)

            await self._publisher.publish(
                Event(
                    event_type=EventType.WORKFLOW_FAILED,
                    metadata=EventMetadata(
                        workflow_id=workflow.id,
                        execution_id=execution.execution_id,
                        source="WorkflowEngine",
                    ),
                    payload={
                        "error": str(exc),
                    },
                )
            )

            return WorkflowResult(
                success=False,
                workflow_id=workflow.id,
                execution_id=execution.execution_id,
                error=str(exc),
                started_at=execution.started_at,
                completed_at=execution.completed_at,
                execution_time_ms=(
                    execution.completed_at - execution.started_at
                ).total_seconds()
                * 1000,
            )
            
        finally:
            await self._hooks.after_workflow(
                workflow=workflow,
                context=execution.context
            )

    def _validate_workflow(
        self,
        workflow: WorkflowDefinition,
    ) -> None:
        """
        Validate workflow before execution.
        """

        if not workflow.enabled:
            raise ValueError(
                f"Workflow '{workflow.id}' is disabled."
            )

        if not workflow.steps:
            raise ValueError(
                "Workflow contains no steps."
            )

        step_ids: set[str] = set()

        for step in workflow.steps:

            if step.id in step_ids:
                raise ValueError(
                    f"Duplicate workflow step '{step.id}'."
                )

            step_ids.add(step.id)