"""
Event Dependencies.
"""

from __future__ import annotations

from functools import lru_cache

from app.events.event_bus import EventBus
from app.events.event_dispatcher import EventDispatcher
from app.events.event_publisher import EventPublisher
from app.events.event_registry import EventRegistry


@lru_cache
def get_event_registry() -> EventRegistry:
    """
    Return the shared Event Registry.
    """

    registry = EventRegistry()

    return registry


@lru_cache
def get_event_dispatcher() -> EventDispatcher:
    """
    Return the shared Event Dispatcher.
    """

    return EventDispatcher(
        registry=get_event_registry(),
    )


@lru_cache
def get_event_bus() -> EventBus:
    """
    Return the shared Event Bus.
    """

    return EventBus(
        dispatcher=get_event_dispatcher(),
    )


@lru_cache
def get_event_publisher() -> EventPublisher:
    """
    Return the shared Event Publisher.
    """

    return EventPublisher(
        event_bus=get_event_bus(),
    )