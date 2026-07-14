from __future__ import annotations

from collections.abc import Iterable

from app.agent.multi_agent.models.agent_descriptor import (
    AgentCapability,
    AgentDescriptor,
    AgentStatus,
)


class AgentRegistry:
    """
    Central registry for all available agents.

    The registry is responsible for:

    - Agent registration
    - Agent discovery
    - Capability lookup
    - Priority ordering
    - Availability filtering

    The registry intentionally contains no execution logic.
    """

    def __init__(self) -> None:
        self._agents: dict[str, AgentDescriptor] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        descriptor: AgentDescriptor,
    ) -> None:
        """
        Register an agent.

        Raises:
            ValueError:
                If the agent already exists.
        """

        if descriptor.agent_id in self._agents:
            raise ValueError(
                f"Agent '{descriptor.agent_id}' is already registered."
            )

        self._agents[descriptor.agent_id] = descriptor

    def unregister(
        self,
        agent_id: str,
    ) -> None:
        """
        Remove an agent from the registry.
        """

        self._agents.pop(agent_id, None)

    def clear(self) -> None:
        """
        Remove all registered agents.
        """

        self._agents.clear()

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        agent_id: str,
    ) -> AgentDescriptor | None:
        """
        Retrieve an agent by id.
        """

        return self._agents.get(agent_id)

    def exists(
        self,
        agent_id: str,
    ) -> bool:
        """
        Returns True if an agent exists.
        """

        return agent_id in self._agents

    def all(self) -> list[AgentDescriptor]:
        """
        Returns all registered agents.
        """

        return list(self._agents.values())

    def active(self) -> list[AgentDescriptor]:
        """
        Returns active agents ordered by priority.
        """

        return sorted(
            (
                agent
                for agent in self._agents.values()
                if agent.status == AgentStatus.ACTIVE
            ),
            key=lambda agent: agent.priority,
        )

    # ------------------------------------------------------------------
    # Capability Lookup
    # ------------------------------------------------------------------

    def by_capability(
        self,
        capability: AgentCapability,
    ) -> list[AgentDescriptor]:
        """
        Find all agents supporting a capability.
        """

        return sorted(
            (
                agent
                for agent in self.active()
                if capability in agent.capabilities
            ),
            key=lambda agent: agent.priority,
        )

    def by_capabilities(
        self,
        capabilities: Iterable[AgentCapability],
        *,
        match_all: bool = True,
    ) -> list[AgentDescriptor]:
        """
        Lookup agents by multiple capabilities.

        Args:
            capabilities:
                Required capabilities.

            match_all:
                True -> every capability must exist.

                False -> any capability may exist.
        """

        required = set(capabilities)

        if not required:
            return self.active()

        matches: list[AgentDescriptor] = []

        for agent in self.active():

            supported = set(agent.capabilities)

            if match_all:

                if required.issubset(supported):
                    matches.append(agent)

            else:

                if supported.intersection(required):
                    matches.append(agent)

        return matches

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def count(self) -> int:
        """
        Number of registered agents.
        """

        return len(self._agents)

    def is_empty(self) -> bool:
        """
        Returns True if no agents are registered.
        """

        return not self._agents

    def capabilities(self) -> set[AgentCapability]:
        """
        Returns all registered capabilities.
        """

        capabilities: set[AgentCapability] = set()

        for agent in self._agents.values():
            capabilities.update(agent.capabilities)

        return capabilities

    def summary(self) -> dict:
        """
        Registry statistics.
        """

        return {
            "registered_agents": self.count(),
            "active_agents": len(self.active()),
            "capabilities": sorted(
                capability.value
                for capability in self.capabilities()
            ),
        }