"""
Reflection Executor.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.reflection.models.reflection_context import ReflectionContext
from app.reflection.models.reflection_result import ReflectionResult
from app.reflection.models.reflection_status import (
    ReflectionDecision,
)


class ReflectionExecutor:
    """
    Executes reflection logic.
    """

    async def execute(
        self,
        context: ReflectionContext,
    ) -> ReflectionResult:
        """
        Evaluate execution outcome and determine the next action.
        """

        started = datetime.now(UTC)

        decision = ReflectionDecision.CONTINUE
        confidence = 1.0
        reason = "Execution completed successfully."

        recommendations: list[str] = []

        payload = context.event_payload

        #
        # Runtime Failure
        #
        if payload.get("success") is False:

            decision = ReflectionDecision.RETRY
            confidence = 0.85
            reason = payload.get(
                "error",
                "Execution failed.",
            )

            recommendations.append(
                "Retry the failed step."
            )

        #
        # Slow execution
        #
        execution_time = payload.get(
            "execution_time_ms",
        )

        if (
            execution_time is not None
            and execution_time > 10000
        ):

            confidence -= 0.10

            recommendations.append(
                "Execution exceeded expected SLA."
            )

        #
        # Escalation Example
        #
        if payload.get(
            "requires_human",
        ):

            decision = (
                ReflectionDecision.HUMAN_APPROVAL
            )

            confidence = 0.95

            reason = (
                "Human approval required."
            )

        completed = datetime.now(
            UTC,
        )

        return ReflectionResult(
            success=True,
            decision=decision,
            confidence=confidence,
            reason=reason,
            recommendations=recommendations,
            metadata=context.metadata,
            started_at=started,
            completed_at=completed,
            execution_time_ms=(
                completed - started
            ).total_seconds()
            * 1000,
        )