"""
Event Publisher.
"""

from __future__ import annotations

from app.events.event_bus import EventBus
from app.events.models.event import Event


class EventPublisher:
    """
    Publishes events to the event bus.
    """

    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self._event_bus = event_bus

    async def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event.
        """

        await self._event_bus.publish(
            event,
        )