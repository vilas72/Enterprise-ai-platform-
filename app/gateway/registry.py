"""
Enterprise Gateway Agent Registry.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Any

from app.gateway.exceptions import (
    AgentNotFoundError,
    GatewayRegistrationError,
)

logger = logging.getLogger(__name__)


class GatewayRegistry:
    """
    Registry for enterprise business agents.

    Responsible for:

    - Registering agents
    - Unregistering agents
    - Agent lookup
    - Capability lookup
    """

    def __init__(self) -> None:

        self._agents: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        agent: Any,
    ) -> None:
        """
        Register an agent.
        """

        if name in self._agents:
            raise GatewayRegistrationError(
                f"Agent '{name}' is already registered."
            )

        logger.info(
            "Registering gateway agent '%s'.",
            name,
        )

        self._agents[name] = agent

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove an agent.
        """

        self._agents.pop(
            name,
            None,
        )

        logger.info(
            "Unregistered gateway agent '%s'.",
            name,
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Any:
        """
        Retrieve an agent by name.
        """

        try:

            return self._agents[name]

        except KeyError as exc:

            raise AgentNotFoundError(
                f"Agent '{name}' not found."
            ) from exc

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if an agent exists.
        """

        return name in self._agents

    # ------------------------------------------------------------------
    # Capability Discovery
    # ------------------------------------------------------------------

    def find_by_capability(
        self,
        capability: str,
    ) -> Any:
        """
        Find an agent supporting a capability.
        """

        for agent in self._agents.values():

            if hasattr(agent, "supports") and agent.supports(capability):
               return agent

        raise AgentNotFoundError(
            f"No registered agent supports "
            f"'{capability}'."
        )

    def supported_capabilities(
        self,
    ) -> dict[str, list[str]]:
        """
        Return capabilities of every registered agent.
        """

        capabilities: dict[str, list[str]] = {}

        for name, agent in self._agents.items():

            capabilities[name] = [
                capability.value
                if hasattr(capability, "value")
                else str(capability)
                for capability in agent.supported_capabilities
            ]

        return capabilities

    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------

    def agents(
        self,
    ) -> Iterable[Any]:
        """
        Return all registered agents.
        """

        return self._agents.values()

    def names(
        self,
    ) -> list[str]:
        """
        Return registered agent names.
        """

        return list(
            self._agents.keys()
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all registered agents.
        """

        self._agents.clear()

        logger.info(
            "Gateway registry cleared."
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._agents
        )

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(name)
    
    def agent_names(
        self,
    ) -> list[str]:
        """
        Return all registered agent names.
        """

        return self.names()
    
    def registered_agents(
        self,
    ) -> dict[str, Any]:
        """
        Return registered agents.
        """

        return self._agents.copy()