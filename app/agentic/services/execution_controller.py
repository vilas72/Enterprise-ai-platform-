from __future__ import annotations

from app.agent.multi_agent.coordinator.agent_coordinator import (
    AgentCoordinator,
)
from app.agent.multi_agent.models.collaboration_request import (
    CollaborationRequest,
)
from app.agent.multi_agent.models.team_result import TeamResult
from app.agentic.models.goal import Goal
from app.agentic.services.goal_manager import GoalManager
from app.agentic.services.reflection_service import ReflectionService
from app.agentic.services.replanning_service import (
    ReplanningService,
)
from app.agentic.services.self_evaluator import SelfEvaluator


class ExecutionController:
    """
    Controls autonomous execution of enterprise goals.

    Responsibilities
    ----------------
    - Goal lifecycle
    - Multi-agent execution
    - Reflection
    - Self evaluation
    - Replanning
    """

    DEFAULT_MAX_EXECUTION_CYCLES = 5

    def __init__(
        self,
        goal_manager: GoalManager,
        coordinator: AgentCoordinator,
        reflection_service: ReflectionService,
        evaluator: SelfEvaluator,
        replanning_service: ReplanningService,
    ) -> None:

        self._goal_manager = goal_manager
        self._coordinator = coordinator
        self._reflection_service = reflection_service
        self._evaluator = evaluator
        self._replanning_service = replanning_service

    async def execute(
        self,
        goal: Goal,
    ) -> TeamResult:

        self._goal_manager.create_goal(goal)

        request = CollaborationRequest(
            query=goal.title,
            context={
                "goal": goal,
            },
            metadata=goal.metadata,
        )

        cycles = 0

        while True:

            cycles += 1

            if cycles > self.DEFAULT_MAX_EXECUTION_CYCLES:
                self._goal_manager.fail_goal(goal)
                raise RuntimeError(
                    "Maximum execution cycles exceeded."
                )

            self._goal_manager.start_execution(goal)

            result = await self._coordinator.collaborate(
                request,
            )

            reflection = self._reflection_service.reflect(
                goal,
                result,
            )

            evaluation = self._evaluator.evaluate(
                goal,
                result,
            )

            if (
                not reflection["requires_replanning"]
                and evaluation["successful"]
            ):
                self._goal_manager.complete_goal(goal)
                return result

            request = (
                self._replanning_service.prepare_replan(
                    goal,
                    result,
                )
            )