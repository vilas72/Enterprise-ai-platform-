"""
Event Registry.
"""

from __future__ import annotations

from collections import defaultdict

from app.events.event_subscriber import EventSubscriber
from app.events.models.event import Event
from app.events.models.event_type import EventType


class EventRegistry:
    """
    Registry for event subscribers.
    """

    def __init__(self) -> None:
        self._subscribers: dict[
            EventType,
            list[EventSubscriber],
        ] = defaultdict(list)

    def register(
        self,
        event_type: EventType,
        subscriber: EventSubscriber,
    ) -> None:
        """
        Register a subscriber.
        """

        self._subscribers[event_type].append(
            subscriber,
        )

    def unregister(
        self,
        event_type: EventType,
        subscriber: EventSubscriber,
    ) -> None:
        """
        Remove a subscriber.
        """

        if subscriber in self._subscribers[event_type]:
            self._subscribers[event_type].remove(
                subscriber,
            )

    def get_subscribers(
        self,
        event_type: EventType,
    ) -> list[EventSubscriber]:
        """
        Return subscribers for an event.
        """

        return self._subscribers.get(
            event_type,
            [],
        )

    async def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event.
        """

        for subscriber in self.get_subscribers(
            event.event_type,
        ):
            await subscriber.handle(
                event,
            )