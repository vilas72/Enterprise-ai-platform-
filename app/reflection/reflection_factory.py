"""
Reflection Factory.
"""

from __future__ import annotations

from app.events.event_publisher import EventPublisher

from app.reflection.reflection_engine import ReflectionEngine
from app.reflection.reflection_registry import ReflectionRegistry


class ReflectionFactory:
    """
    Factory for Reflection Engine.
    """

    @staticmethod
    def create(
        publisher: EventPublisher,
    ) -> ReflectionEngine:
        """
        Create Reflection Engine.
        """

        registry = ReflectionRegistry()

        return ReflectionEngine(
            executor=registry.get_executor(),
            publisher=publisher,
        )