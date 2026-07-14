from __future__ import annotations

from app.agent.multi_agent.coordinator.agent_registry import AgentRegistry
from app.agent.multi_agent.models.agent_descriptor import (
    AgentCapability,
    AgentDescriptor,
)
from app.agent.multi_agent.models.collaboration_request import (
    CollaborationRequest,
)


class AgentSelector:
    """
    Selects the most appropriate agents for a collaboration request.

    Selection is based on:

    - Preferred agents
    - Required capabilities
    - Agent priority
    - Agent availability

    The selector is intentionally deterministic and contains
    no execution logic.
    """

    def __init__(
        self,
        registry: AgentRegistry,
    ) -> None:
        self._registry = registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def select(
        self,
        request: CollaborationRequest,
    ) -> list[AgentDescriptor]:
        """
        Select agents for a collaboration request.
        """

        # Preferred agents always win if available.
        preferred = self._select_preferred(request)

        if preferred:
            return preferred

        # Otherwise perform capability lookup.
        capabilities = request.required_capabilities

        if capabilities:
            return self.select_by_capabilities(capabilities)

        # Default to all active agents.
        return self._registry.active()

    def select_one(
        self,
        capability: AgentCapability,
    ) -> AgentDescriptor | None:
        """
        Select the highest-priority agent for a capability.
        """

        agents = self._registry.by_capability(capability)

        if not agents:
            return None

        return agents[0]

    def select_by_capabilities(
        self,
        capabilities: set[AgentCapability] | frozenset[AgentCapability],
        *,
        match_all: bool = False,
    ) -> list[AgentDescriptor]:
        """
        Select agents supporting one or more capabilities.
        """

        return self._registry.by_capabilities(
            capabilities,
            match_all=match_all,
        )

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _select_preferred(
        self,
        request: CollaborationRequest,
    ) -> list[AgentDescriptor]:
        """
        Resolve preferred agents.
        """

        selected: list[AgentDescriptor] = []

        for agent_id in request.preferred_agents:

            agent = self._registry.get(agent_id)

            if agent is None:
                continue

            if not agent.is_active:
                continue

            selected.append(agent)

        return sorted(
            selected,
            key=lambda agent: agent.priority,
        )