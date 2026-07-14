from __future__ import annotations

from app.agent.multi_agent.models.collaboration_request import (
    CollaborationRequest,
)
from app.agent.multi_agent.models.team_result import TeamResult
from app.agentic.models.goal import Goal
from app.agentic.services.goal_manager import GoalManager
from app.agentic.services.reflection_service import ReflectionService
from app.agentic.services.self_evaluator import SelfEvaluator


class ReplanningService:
    """
    Determines whether a goal requires another execution cycle.

    Responsibilities:
    - Analyze reflection
    - Analyze self-evaluation
    - Update goal lifecycle
    - Build the next collaboration request
    """

    def __init__(
        self,
        goal_manager: GoalManager,
        reflection_service: ReflectionService,
        evaluator: SelfEvaluator,
    ) -> None:

        self._goal_manager = goal_manager
        self._reflection_service = reflection_service
        self._evaluator = evaluator

    def requires_replanning(
        self,
        goal: Goal,
        result: TeamResult,
    ) -> bool:
        """
        Determine whether replanning is required.
        """

        reflection = self._reflection_service.reflect(
            goal,
            result,
        )

        evaluation = self._evaluator.evaluate(
            goal,
            result,
        )

        return (
            reflection["requires_replanning"]
            or not evaluation["successful"]
        )

    def prepare_replan(
        self,
        goal: Goal,
        result: TeamResult,
    ) -> CollaborationRequest:
        """
        Prepare the next collaboration request.
        """

        self._goal_manager.start_replanning(goal)

        reflection = self._reflection_service.reflect(
            goal,
            result,
        )

        evaluation = self._evaluator.evaluate(
            goal,
            result,
        )

        context = {
            "goal": goal,
            "previous_result": result,
            "reflection": reflection,
            "evaluation": evaluation,
            "replanning": True,
        }

        return CollaborationRequest(
            conversation_id=None,
            user_id=None,
            query=goal.title,
            context=context,
            metadata={
                **goal.metadata,
                "execution_cycle": "replan",
            },
        )

    def complete_replanning(
        self,
        goal: Goal,
    ) -> None:
        """
        Move the goal back into execution.
        """

        self._goal_manager.start_execution(goal)