"""
Enterprise execution engine.
"""

from __future__ import annotations

from app.agents.execution.execution_result import ExecutionResult
from app.agents.execution.step_handler import StepHandler
from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_plan import AgentPlan


class ExecutionEngine:
    """
    Executes an AgentPlan by delegating each step to
    the appropriate StepHandler.
    """

    def __init__(
        self,
        handlers: list[StepHandler],
    ) -> None:

        self._handlers = handlers

    def execute(
        self,
        plan: AgentPlan,
        context: AgentContext,
    ) -> ExecutionResult:

        executed = 0

        for step in plan.steps:

            handler = next(
                (
                    h
                    for h in self._handlers
                    if h.supports(step)
                ),
                None,
            )

            if handler is None:

                raise RuntimeError(
                    f"No handler registered for '{step.action}'."
                )

            handler.execute(
                step,
                context,
            )

            executed += 1

        return ExecutionResult(
            success=True,
            context=context,
            executed_steps=executed,
        )