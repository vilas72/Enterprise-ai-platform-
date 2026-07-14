from __future__ import annotations

from app.agent.multi_agent.coordinator.agent_selector import AgentSelector
from app.agent.multi_agent.coordinator.result_aggregator import (
    ResultAggregator,
)
from app.agent.multi_agent.coordinator.task_dispatcher import (
    TaskDispatcher,
)
from app.agent.multi_agent.coordinator.task_router import TaskRouter
from app.agent.multi_agent.models.collaboration_request import (
    CollaborationRequest,
)
from app.agent.multi_agent.models.team_result import TeamResult


class AgentCoordinator:
    """
    Coordinates multi-agent collaboration.

    Responsibilities:

    - Agent selection
    - Task routing
    - Task dispatch
    - Result aggregation

    Does NOT perform planning,
    reasoning,
    tool execution,
    or response generation.
    """

    def __init__(
        self,
        selector: AgentSelector,
        router: TaskRouter,
        dispatcher: TaskDispatcher,
        aggregator: ResultAggregator,
    ) -> None:

        self._selector = selector
        self._router = router
        self._dispatcher = dispatcher
        self._aggregator = aggregator

    async def collaborate(
        self,
        request: CollaborationRequest,
    ) -> TeamResult:
        """
        Execute a collaboration request.
        """

        agents = self._selector.select(request)

        if not agents:

            return self._aggregator.aggregate(
                collaboration_id=request.collaboration_id,
                results=[],
            )

        tasks = self._router.route(
            request=request,
            agents=agents,
        )

        results = await self._dispatcher.dispatch(
            tasks,
        )

        return self._aggregator.aggregate(
            collaboration_id=request.collaboration_id,
            results=results,
        )