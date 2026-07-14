from __future__ import annotations

from app.agent.multi_agent.coordinator.agent_coordinator import AgentCoordinator
from app.agent.multi_agent.coordinator.agent_registry import AgentRegistry
from app.agent.multi_agent.coordinator.agent_selector import AgentSelector
from app.agent.multi_agent.coordinator.result_aggregator import ResultAggregator
from app.agent.multi_agent.coordinator.task_dispatcher import TaskDispatcher
from app.agent.multi_agent.coordinator.task_router import TaskRouter
from app.agent.multi_agent.services.collaboration_service import CollaborationService


class MultiAgentRuntime:
    """Factory-style runtime wiring for the multi-agent bounded context."""

    @staticmethod
    def build() -> CollaborationService:
        coordinator = AgentCoordinator(
            registry=AgentRegistry(),
            selector=AgentSelector(),
            router=TaskRouter(),
            dispatcher=TaskDispatcher(),
            aggregator=ResultAggregator(),
        )
        return CollaborationService(coordinator)
