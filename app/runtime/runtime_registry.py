"""
Runtime Registry.
"""

from __future__ import annotations

from app.runtime.agent_runtime import AgentRuntime


class RuntimeRegistry:
    """
    Registry of runtime instances.
    """

    def __init__(self) -> None:

        self._runtimes: dict[str, AgentRuntime] = {}

    def register(
        self,
        name: str,
        runtime: AgentRuntime,
    ) -> None:
        """
        Register a runtime.
        """

        self._runtimes[name] = runtime

    def get(
        self,
        name: str,
    ) -> AgentRuntime:
        """
        Retrieve a runtime.
        """

        return self._runtimes[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check runtime exists.
        """

        return name in self._runtimes

    def runtimes(self) -> list[str]:
        """
        Registered runtimes.
        """

        return list(self._runtimes.keys())