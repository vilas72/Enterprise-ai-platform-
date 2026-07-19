"""
Enterprise Agent Runtime.
"""

from __future__ import annotations
from datetime import datetime
import uuid

from app.events.event_publisher import EventPublisher
from app.gateway.models import GatewayRequest
from app.runtime.models.runtime_context import RuntimeContext
from app.runtime.models.runtime_result import RuntimeResult
from app.runtime.runtime_executor import RuntimeExecutor


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

        execution_id = str(uuid.uuid4())
        started = datetime.now()

        context = RuntimeContext(
            execution_id=execution_id,
            workflow_id=workflow_id,
            agent=agent,
            capability=capability,
            request=request,
        )

        result = await self._executor.execute(context)

        completed = datetime.now()

        result.started_at = started
        result.completed_at = completed
        result.execution_time_ms = (
            completed - started
        ).total_seconds() * 1000

        return result