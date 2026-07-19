"""
Enterprise Agent Runtime.
"""

from __future__ import annotations

from asyncio.log import logger
import uuid
import traceback
from datetime import UTC, datetime

from app.events.models.event_metadata import EventMetadata
from app.runtime.models.runtime_context import RuntimeContext
from app.gateway.models import GatewayRequest
from app.runtime.models.runtime_execution import RuntimeExecution
from app.runtime.models.runtime_result import RuntimeResult
from app.runtime.models.runtime_status import (
    RuntimeExecutionStatus,
)
from app.runtime.runtime_executor import RuntimeExecutor
from app.events.event_publisher import EventPublisher
from app.events.models.event import Event
from app.events.models.event_metadata import EventMetadata
from app.events.models.event_type import EventType
from app.events.models.event_source import EventSource

class AgentRuntime:
    """
    Enterprise Agent Runtime.
    """

    def __init__(
        self,
        executor: RuntimeExecutor,
        publisher: EventPublisher,
    ) -> None:

        self._executor = executor
        self._publisher = publisher

    async def execute(
        self,
        *,
        agent: str,
        capability: str,
        request: GatewayRequest,
        workflow_id: str | None = None,
    ) -> RuntimeResult:
        """
        Execute an agent capability.
        """

        execution_id = str(
            uuid.uuid4()
        )

        started = datetime.now(
            UTC,
        )

        context = RuntimeContext(
            execution_id=execution_id,
            workflow_id=workflow_id,
            agent=agent,
            capability=request.capability,
            request=request,
        )

        execution = RuntimeExecution(
            execution_id=execution_id,
            context=context,
            status=RuntimeExecutionStatus.RUNNING,
            started_at=started,
        )
        
        await self._publisher.publish(
            Event(
                event_type=EventType.RUNTIME_STARTED,
                metadata=EventMetadata(
                    workflow_id=workflow_id,
                    execution_id=execution_id,
                    agent=agent,
                    capability=capability,
                    source=EventSource.AGENT_RUNTIME,
                ),
            )
        )

        try:

            result = await self._executor.execute(
                context,
            )

            completed = datetime.now(
                UTC,
            )

            execution.status = (
                RuntimeExecutionStatus.COMPLETED
            )

            execution.completed_at = completed

            result.started_at = started
            result.completed_at = completed

            result.execution_time_ms = (
                completed - started
            ).total_seconds() * 1000

            await self._publisher.publish(
                Event(
                    event_type=EventType.RUNTIME_COMPLETED,
                    metadata=EventMetadata(
                        workflow_id=workflow_id,
                        execution_id=execution_id,
                        agent=agent,
                        capability=capability,
                        source=EventSource.AGENT_RUNTIME,
                    ),
                    payload={
                        "success": True,
                        "error": None,
                    },
                )
            )
            return result

        except Exception as exc:

            logger.exception("Unhandled exception")
            print(traceback.format_exc())
     
            completed = datetime.now(
                UTC,
            )

            execution.status = (
                RuntimeExecutionStatus.FAILED
            )

            execution.completed_at = completed
            execution.error = str(exc)
            
          
            return RuntimeResult(
                success=False,
                execution_id=execution_id,
                agent=agent,
                capability=capability,
                error=str(exc),
                started_at=started,
                completed_at=completed,
                execution_time_ms=(
                    completed - started
                ).total_seconds()
                * 1000,
            )