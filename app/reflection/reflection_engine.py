"""
Reflection Engine.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.events.event_publisher import EventPublisher
from app.events.models.event import Event
from app.events.models.event_metadata import EventMetadata
from app.events.models.event_type import EventType

from app.reflection.models.reflection_context import (
    ReflectionContext,
)
from app.reflection.models.reflection_result import (
    ReflectionResult,
)
from app.reflection.reflection_executor import (
    ReflectionExecutor,
)


class ReflectionEngine:
    """
    Enterprise Reflection Engine.
    """

    def __init__(
        self,
        executor: ReflectionExecutor,
        publisher: EventPublisher,
    ) -> None:

        self._executor = executor
        self._publisher = publisher

    async def execute(
        self,
        context: ReflectionContext,
    ) -> ReflectionResult:
        """
        Execute reflection.
        """

        execution_id = str(
            uuid.uuid4(),
        )

        await self._publisher.publish(
            Event(
                event_type=EventType.REFLECTION_STARTED,
                metadata=EventMetadata(
                    workflow_id=context.workflow_id,
                    execution_id=execution_id,
                    source="ReflectionEngine",
                ),
            )
        )

        try:

            result = await self._executor.execute(
                context,
            )

            await self._publisher.publish(
                Event(
                    event_type=EventType.REFLECTION_COMPLETED,
                    metadata=EventMetadata(
                        workflow_id=context.workflow_id,
                        execution_id=execution_id,
                        source="ReflectionEngine",
                    ),
                    payload={
                        "decision": result.decision.value,
                        "confidence": result.confidence,
                    },
                )
            )

            return result

        except Exception as exc:

            await self._publisher.publish(
                Event(
                    event_type=EventType.REFLECTION_FAILED,
                    metadata=EventMetadata(
                        workflow_id=context.workflow_id,
                        execution_id=execution_id,
                        source="ReflectionEngine",
                    ),
                    payload={
                        "error": str(exc),
                    },
                )
            )

            raise