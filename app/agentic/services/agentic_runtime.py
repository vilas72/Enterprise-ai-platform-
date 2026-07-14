from __future__ import annotations

from app.agent.multi_agent.models.team_result import TeamResult
from app.agentic.models.goal import Goal
from app.agentic.services.execution_controller import (
    ExecutionController,
)
from app.agentic.services.goal_manager import GoalManager


class AgenticRuntime:
    """
    Public entry point for the Agentic Runtime.

    Responsibilities
    ----------------
    - Goal lifecycle orchestration
    - Autonomous execution
    - Goal state management

    This class acts as the Facade over the complete
    Agentic Runtime.
    """

    def __init__(
        self,
        goal_manager: GoalManager,
        execution_controller: ExecutionController,
    ) -> None:

        self._goal_manager = goal_manager
        self._execution_controller = execution_controller

    async def run(
        self,
        goal: Goal,
    ) -> TeamResult:
        """
        Execute a business goal.
        """

        self._goal_manager.create_goal(goal)

        return await self._execution_controller.execute(
            goal,
        )

    async def resume(
        self,
        goal: Goal,
    ) -> TeamResult:
        """
        Resume a paused goal.
        """

        return await self._execution_controller.execute(
            goal,
        )

    def cancel(
        self,
        goal: Goal,
    ) -> Goal:
        """
        Cancel an executing goal.
        """

        self._goal_manager.cancel_goal(goal)

        return goal

    def complete(
        self,
        goal: Goal,
    ) -> Goal:
        """
        Mark a goal as completed.
        """

        self._goal_manager.complete_goal(goal)

        return goal

    def fail(
        self,
        goal: Goal,
    ) -> Goal:
        """
        Mark a goal as failed.
        """

        self._goal_manager.fail_goal(goal)

        return goal