"""
Event Bus.
"""

from __future__ import annotations

from app.events.event_dispatcher import EventDispatcher
from app.events.models.event import Event


class EventBus:
    """
    Central event bus for publishing platform events.
    """

    def __init__(
        self,
        dispatcher: EventDispatcher,
    ) -> None:
        self._dispatcher = dispatcher

    async def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event.
        """

        await self._dispatcher.dispatch(
            event,
        )