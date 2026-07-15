"""
Enterprise Reflection Engine.
"""

from __future__ import annotations

from app.agents.execution.execution_result import ExecutionResult
from app.agents.models.agent_plan import AgentPlan


class ReflectionEngine:
    """
    Reflection component.

    Future Responsibilities
    -----------------------

    - Self evaluation
    - Retry planning
    - Confidence scoring
    - Error recovery
    - LLM critique
    """

    def reflect(
        self,
        plan: AgentPlan,
        result: ExecutionResult,
    ) -> None:
        """
        Reflect on execution.

        Current implementation intentionally keeps
        this as a no-op.
        """

        return


class DefaultReflectionEngine(ReflectionEngine):
    """Backward-compatible default reflection engine alias."""
