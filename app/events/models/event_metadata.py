"""
Event Metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class EventMetadata:
    """
    Common metadata attached to every event.
    """

    workflow_id: str | None = None
    execution_id: str | None = None
    correlation_id: str | None = None
    agent: str | None = None
    capability: str | None = None
    source: str | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    attributes: dict[str, Any] = field(default_factory=dict)