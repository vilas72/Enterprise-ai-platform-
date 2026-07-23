"""
Event Dispatcher.
"""

from __future__ import annotations

from app.events.event_registry import EventRegistry
from app.events.models.event import Event


class EventDispatcher:
    """
    Dispatches events to subscribers.
    """

    def __init__(
        self,
        registry: EventRegistry,
    ) -> None:
        self._registry = registry

    async def dispatch(
        self,
        event: Event,
    ) -> None:
        """
        Dispatch an event.
        """

        await self._registry.publish(
            event,
        )