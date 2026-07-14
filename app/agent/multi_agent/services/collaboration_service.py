from __future__ import annotations

from app.agent.multi_agent.coordinator.agent_coordinator import AgentCoordinator
from app.agent.multi_agent.models.collaboration_request import CollaborationRequest
from app.agent.multi_agent.models.collaboration_result import CollaborationResult


class CollaborationService:
    """Application service for multi-agent collaboration flows."""

    def __init__(self, coordinator: AgentCoordinator) -> None:
        self._coordinator = coordinator

    async def collaborate(self, request: CollaborationRequest) -> CollaborationResult:
        return await self._coordinator.execute(request)
