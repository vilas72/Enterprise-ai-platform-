"""
Platform Event.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.events.models.event_metadata import EventMetadata
from app.events.models.event_type import EventType


@dataclass(slots=True)
class Event:
    """
    Platform event.
    """

    event_type: EventType
    metadata: EventMetadata = field(default_factory=EventMetadata)
    payload: dict[str, Any] = field(default_factory=dict)