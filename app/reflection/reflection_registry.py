"""
Reflection Registry.
"""

from __future__ import annotations

from app.reflection.reflection_executor import ReflectionExecutor


class ReflectionRegistry:
    """
    Registry for reflection executors.
    """

    def __init__(self) -> None:
        self._executor = ReflectionExecutor()

    def get_executor(self) -> ReflectionExecutor:
        """
        Return the reflection executor.
        """

        return self._executor