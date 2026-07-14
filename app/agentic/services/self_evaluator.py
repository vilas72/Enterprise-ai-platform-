from __future__ import annotations

from app.agent.multi_agent.models.team_result import TeamResult
from app.agentic.models.goal import Goal


class SelfEvaluator:
    """
    Evaluates whether a Goal has actually been achieved.

    Unlike ReflectionService, this evaluates business success,
    not execution success.
    """

    def evaluate(
        self,
        goal: Goal,
        result: TeamResult,
    ) -> dict[str, object]:
        """
        Evaluate goal completion.
        """

        criteria_results = [
            {
                "name": criteria.name,
                "satisfied": criteria.satisfied,
            }
            for criteria in goal.success_criteria
        ]

        satisfied = sum(
            1
            for criteria in goal.success_criteria
            if criteria.satisfied
        )

        total = len(goal.success_criteria)

        score = (
            (satisfied / total) * 100
            if total > 0
            else 100
        )

        successful = (
            score == 100
            and result.success_rate == 1.0
        )

        return {
            "goal_id": goal.goal_id,
            "goal_title": goal.title,
            "goal_status": goal.status.value,
            "evaluation_score": score,
            "successful": successful,
            "criteria": criteria_results,
            "execution_success_rate": result.success_rate,
            "agent_statistics": {
                "total": result.total_agents,
                "successful": result.successful_agents,
                "failed": result.failed_agents,
            },
            "recommendation": self._recommend(
                successful,
                score,
            ),
        }

    def evaluate_success(
        self,
        goal: Goal,
    ) -> bool:
        """
        Returns True if all success criteria are satisfied.
        """

        return all(
            criteria.satisfied
            for criteria in goal.success_criteria
        )

    def _recommend(
        self,
        successful: bool,
        score: float,
    ) -> str:

        if successful:
            return "Goal completed successfully."

        if score >= 80:
            return (
                "Goal mostly completed. "
                "Minor improvements recommended."
            )

        if score >= 50:
            return (
                "Goal partially completed. "
                "Replanning recommended."
            )

        return (
            "Goal failed. "
            "Replanning required."
        )