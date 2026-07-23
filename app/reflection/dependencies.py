"""
Reflection Dependencies.
"""

from __future__ import annotations

from functools import lru_cache

from app.events.dependencies import get_event_publisher
from app.reflection.reflection_factory import ReflectionFactory
from app.reflection.reflection_engine import ReflectionEngine


@lru_cache
def get_reflection_engine() -> ReflectionEngine:
    """
    Return singleton Reflection Engine.
    """

    return ReflectionFactory.create(
        publisher=get_event_publisher(),
    )