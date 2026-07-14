"""
Enterprise Agent Runtime.
"""

from __future__ import annotations

from app.agents.executor.agent_executor import AgentExecutor
from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_request import AgentRequest
from app.agents.models.agent_response import AgentResponse
from app.agents.planner.planner import Planner
from app.agents.reflection.reflection_engine import ReflectionEngine


class AgentRuntime:
    """
    Enterprise Agent Runtime.

    Coordinates the complete lifecycle of an Agent execution.

    Responsibilities
    ----------------

    - Build execution context
    - Invoke Planner
    - Invoke Executor
    - Invoke Reflection
    - Return AgentResponse

    Future

    - Workflow Engine
    - LangGraph Runtime
    - MCP Runtime
    - Human Approval
    - Multi-Agent Coordination
    """

    def __init__(
        self,
        planner: Planner,
        executor: AgentExecutor,
        reflection_engine: ReflectionEngine,
    ) -> None:

        self._planner = planner
        self._executor = executor
        self._reflection = reflection_engine

    def execute(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        """
        Execute an Agent request.
        """

        #
        # Build Context
        #

        context = AgentContext(
            conversation_id=request.conversation_id,
            user_id=request.user_id,
            tenant_id=request.tenant_id,
        )

        #
        # Planning
        #

        planner_result = self._planner.create_plan(
            request,
            context,
        )

        #
        # Execute Plan
        #

        execution_result, summary = self._executor.execute(
            planner_result.plan,
            context,
        )

        #
        # Reflection
        #

        self._reflection.reflect(
            planner_result.plan,
            execution_result,
        )

        #
        # Build Response
        #

        return AgentResponse(
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            conversation_id=request.conversation_id,
            success=summary.success,
            output=execution_result.output,
            message="Agent execution completed.",
            steps_executed=summary.executed_steps,
            total_steps=planner_result.plan.total_steps,
            execution_time_ms=summary.execution_time_ms,
            metadata=summary.metadata,
        )