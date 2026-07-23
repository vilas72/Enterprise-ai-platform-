"""
Event Subscriber.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.events.models.event import Event


class EventSubscriber(ABC):
    """
    Base class for all event subscribers.
    """

    @abstractmethod
    async def handle(
        self,
        event: Event,
    ) -> None:
        """
        Handle an event.
        """
        raise NotImplementedError