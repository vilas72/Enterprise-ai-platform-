"""
Event Bootstrap.

Creates and wires the Enterprise Event infrastructure.

Dependency Graph

EventDispatcher
        │
        ▼
    EventBus
        │
        ▼
 EventPublisher
"""

from __future__ import annotations

from app.events.event_dispatcher import EventDispatcher
from app.events.event_bus import EventBus
from app.events.event_publisher import EventPublisher
from app.events.event_registry import EventRegistry


#
# Dispatcher
#

event_registry = EventRegistry()

event_dispatcher = EventDispatcher(
    registry=event_registry
)


#
# Event Bus
#

event_bus = EventBus(
    dispatcher=event_dispatcher,
)


#
# Event Publisher
#

event_publisher = EventPublisher(
    event_bus=event_bus,
)

async def initialize_events():
    """
    Initialize the event system.
    """

    await event_dispatcher.initialize() 