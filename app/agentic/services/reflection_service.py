from __future__ import annotations

from app.agent.multi_agent.models.team_result import TeamResult
from app.agentic.models.goal import Goal


class ReflectionService:
    """
    Performs post-execution reflection.

    Responsibilities:
    - Analyze execution outcome
    - Determine whether replanning is required
    - Produce execution insights
    """

    def reflect(
        self,
        goal: Goal,
        result: TeamResult,
    ) -> dict[str, object]:
        """
        Reflect on execution.
        """

        observations: list[str] = []
        recommendations: list[str] = []

        if result.failed_agents > 0:
            observations.append(
                f"{result.failed_agents} agent(s) failed."
            )

            recommendations.append(
                "Retry failed agent tasks."
            )

        if result.success_rate < 1.0:
            observations.append(
                "Execution completed with partial success."
            )

            recommendations.append(
                "Evaluate failed tasks before completion."
            )

        if result.successful_agents == result.total_agents:
            observations.append(
                "Goal completed successfully."
            )

        return {
            "goal_id": goal.goal_id,
            "goal_status": goal.status.value,
            "success_rate": result.success_rate,
            "completed": goal.is_completed,
            "requires_replanning": self.requires_replanning(
                result,
            ),
            "observations": observations,
            "recommendations": recommendations,
        }

    def requires_replanning(
        self,
        result: TeamResult,
    ) -> bool:
        """
        Determine whether replanning should occur.
        """

        return (
            result.failed_agents > 0
            or result.success_rate < 1.0
        )