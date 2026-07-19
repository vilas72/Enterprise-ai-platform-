"""
Runtime Executor.
"""
from __future__ import annotations


from app.gateway.router import GatewayRouter
from app.runtime.models.runtime_context import RuntimeContext
from app.runtime.models.runtime_result import RuntimeResult


class RuntimeExecutor:
    """
    Executes a single runtime request.
    """

    def __init__(
        self,
        router: GatewayRouter,
    ) -> None:

        self._router = router

    async def execute(
        self,
        context: RuntimeContext,
    ) -> RuntimeResult:
        """
        Execute a runtime request.
        """

        agent = self._router.get_agent(
            context.agent,
        )

        agent_request = self._router.build_agent_request(
            agent=agent,
            capability=context.capability,
            request=context.request,
        )

        response = await agent.execute(
            agent_request,
        )
      
        context.response = response

        return RuntimeResult(
            success=response.success,
            execution_id=context.execution_id,
            agent=context.agent,
            capability=context.capability,
            result=response.result,
            metadata=response.metadata.model_dump(),
        )