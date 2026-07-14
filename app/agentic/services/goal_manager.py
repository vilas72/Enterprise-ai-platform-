from __future__ import annotations

from datetime import UTC, datetime
from typing import Iterable

from app.agentic.models.goal import Goal
from app.agentic.models.value_objects.goal_status import GoalStatus
from app.agentic.models.value_objects.objective import Objective


class GoalManager:
    """
    Manages the lifecycle of agentic goals.

    Responsibilities:
    - Goal validation
    - Objective management
    - Progress calculation
    - Goal state transitions
    - Agent assignment

    This service does not execute goals. Execution is delegated to the
    ExecutionController.
    """

    def create_goal(
        self,
        goal: Goal,
    ) -> Goal:
        """
        Validate and initialize a goal.
        """

        self.validate(goal)

        goal.status = GoalStatus.CREATED
        goal.progress = 0.0
        goal.updated_at = datetime.now(UTC)

        return goal

    def validate(
        self,
        goal: Goal,
    ) -> None:
        """
        Validate a goal before execution.
        """

        if not goal.title.strip():
            raise ValueError("Goal title cannot be empty.")

        if not goal.objectives:
            raise ValueError(
                "A goal must contain at least one objective."
            )

        if not goal.success_criteria:
            raise ValueError(
                "At least one success criteria is required."
            )

    def start_planning(
        self,
        goal: Goal,
    ) -> Goal:
        goal.mark_planning()
        return goal

    def start_execution(
        self,
        goal: Goal,
    ) -> Goal:
        goal.mark_executing()
        return goal

    def start_reflection(
        self,
        goal: Goal,
    ) -> Goal:
        goal.mark_reflecting()
        return goal

    def start_replanning(
        self,
        goal: Goal,
    ) -> Goal:
        goal.mark_replanning()
        return goal

    def complete_goal(
        self,
        goal: Goal,
    ) -> Goal:
        goal.mark_completed()
        return goal

    def fail_goal(
        self,
        goal: Goal,
    ) -> Goal:
        goal.mark_failed()
        return goal

    def cancel_goal(
        self,
        goal: Goal,
    ) -> Goal:
        goal.cancel()
        return goal

    def assign_agent(
        self,
        goal: Goal,
        agent_id: str,
    ) -> None:
        goal.assign_agent(agent_id)

    def assign_agents(
        self,
        goal: Goal,
        agent_ids: Iterable[str],
    ) -> None:

        for agent_id in agent_ids:
            goal.assign_agent(agent_id)

    def add_objective(
        self,
        goal: Goal,
        objective: Objective,
    ) -> None:
        goal.add_objective(objective)

    def update_progress(
        self,
        goal: Goal,
    ) -> float:
        """
        Recalculate progress from completed objectives.
        """

        if not goal.objectives:
            goal.update_progress(0.0)
            return 0.0

        completed = sum(
            1
            for objective in goal.objectives
            if objective.completed
        )

        progress = (
            completed / len(goal.objectives)
        ) * 100

        goal.update_progress(progress)

        return progress

    def mark_objective_completed(
        self,
        goal: Goal,
        objective_name: str,
    ) -> None:

        for objective in goal.objectives:

            if objective.name != objective_name:
                continue

            objective.mark_completed()
            break

        self.update_progress(goal)

    def is_completed(
        self,
        goal: Goal,
    ) -> bool:

        return goal.status == GoalStatus.COMPLETED

    def can_execute(
        self,
        goal: Goal,
    ) -> bool:

        return goal.status in {
            GoalStatus.CREATED,
            GoalStatus.PLANNING,
            GoalStatus.REPLANNING,
        }

    def requires_replanning(
        self,
        goal: Goal,
    ) -> bool:

        return goal.status == GoalStatus.REPLANNING