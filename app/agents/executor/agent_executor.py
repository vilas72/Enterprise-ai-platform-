"""
Enterprise Agent Executor.
"""

from __future__ import annotations

import time

from app.agents.execution.execution_engine import ExecutionEngine
from app.agents.execution.execution_result import ExecutionResult
from app.agents.executor.execution_summary import ExecutionSummary
from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_plan import AgentPlan


class AgentExecutor:
    """
    Executes an AgentPlan using the configured
    ExecutionEngine.

    Responsibilities
    ----------------
    - Execute execution plans
    - Measure execution time
    - Produce execution summaries
    - Future:
        * Retry
        * Cancellation
        * Progress Tracking
        * Metrics
        * Parallel Execution
    """

    def __init__(
        self,
        execution_engine: ExecutionEngine,
    ) -> None:

        self._execution_engine = execution_engine

    def execute(
        self,
        plan: AgentPlan,
        context: AgentContext,
    ) -> tuple[ExecutionResult, ExecutionSummary]:

        start = time.perf_counter()

        result = self._execution_engine.execute(
            plan,
            context,
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        summary = ExecutionSummary(
            success=result.success,
            executed_steps=result.executed_steps,
            failed_steps=0,
            skipped_steps=0,
            execution_time_ms=elapsed,
            output=result.output,
            error=result.error,
        )

        return result, summary