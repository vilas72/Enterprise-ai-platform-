"""Agent registry for discovering and managing agents."""

from __future__ import annotations

from typing import Any


class AgentRegistry:
    """
    Central registry for managing agent instances and configurations.

    Supports registration, discovery, and lifecycle management of agents.
    """

    def __init__(self):
        """Initialize the agent registry."""
        self._agents: dict[str, Any] = {}
        self._metadata: dict[str, dict[str, Any]] = {}

    def register(
        self,
        agent_id: str,
        agent: Any,
        metadata: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> None:
        """
        Register an agent in the registry.

        Args:
            agent_id: Unique identifier for the agent
            agent: The agent instance
            metadata: Optional metadata about the agent
            overwrite: Whether to overwrite existing registration

        Raises:
            ValueError: If agent already registered and overwrite is False
        """
        if agent_id in self._agents and not overwrite:
            raise ValueError(f"Agent {agent_id} already registered")

        self._agents[agent_id] = agent
        self._metadata[agent_id] = metadata or {}

    def get(self, agent_id: str) -> Any:
        """
        Retrieve an agent by ID.

        Args:
            agent_id: The agent identifier

        Returns:
            The agent instance

        Raises:
            KeyError: If agent not found
        """
        if agent_id not in self._agents:
            raise KeyError(f"Agent {agent_id} not found")
        return self._agents[agent_id]

    def list_agents(self) -> list[str]:
        """
        List all registered agent IDs.

        Returns:
            Sorted list of agent IDs
        """
        return sorted(self._agents.keys())

    def find_by_tag(self, tag: str) -> list[str]:
        """
        Find agents by metadata tag.

        Args:
            tag: Tag to search for

        Returns:
            List of agent IDs with matching tag
        """
        result = []
        for agent_id, metadata in self._metadata.items():
            if tag in metadata.get("tags", []):
                result.append(agent_id)
        return result

    def get_metadata(self, agent_id: str) -> dict[str, Any]:
        """
        Get metadata for an agent.

        Args:
            agent_id: The agent identifier

        Returns:
            Metadata dictionary
        """
        return self._metadata.get(agent_id, {})

    def unregister(self, agent_id: str) -> None:
        """
        Unregister an agent from the registry.

        Args:
            agent_id: The agent to unregister

        Raises:
            KeyError: If agent not found
        """
        if agent_id not in self._agents:
            raise KeyError(f"Agent {agent_id} not found")
        del self._agents[agent_id]
        del self._metadata[agent_id]
