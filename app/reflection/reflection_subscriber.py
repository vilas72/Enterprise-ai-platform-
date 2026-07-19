"""
Reflection Event Subscriber.
"""

from __future__ import annotations

from app.events.event_subscriber import EventSubscriber
from app.events.models.event import Event

from app.reflection.models.reflection_context import (
    ReflectionContext,
)
from app.reflection.reflection_engine import ReflectionEngine


class ReflectionSubscriber(EventSubscriber):
    """
    Consumes platform events and invokes reflection.
    """

    def __init__(
        self,
        engine: ReflectionEngine,
    ) -> None:

        self._engine = engine

    async def handle(
        self,
        event: Event,
    ) -> None:
        """
        Handle an incoming event.
        """

        context = ReflectionContext(
            workflow_id=event.metadata.workflow_id or "",
            execution_id=event.metadata.execution_id or "",
            event_type=event.event_type.value,
            event_payload=event.payload,
            metadata=event.metadata.attributes,
        )

        await self._engine.execute(
            context,
        )