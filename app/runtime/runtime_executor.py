"""
Runtime Executor.
"""
from __future__ import annotations



from app.runtime.models.runtime_context import RuntimeContext
from app.runtime.models.runtime_result import RuntimeResult
from app.gateway.registry import GatewayRegistry

from app.runtime.agent_request_factory import AgentRequestFactory

class RuntimeExecutor:
    """
    Executes a single runtime request.
    """

    def __init__(
        self,
        registry: GatewayRegistry,
    ) -> None:

        self._registry = registry
        self._request_factory = AgentRequestFactory()

    async def execute(
        self,
        context: RuntimeContext,
    ) -> RuntimeResult:
        """
        Execute a runtime request.
        """
        
        agent = self._registry.get(context.agent)

        if agent is None:
            raise ValueError(
                f"Agent '{context.agent}' is not registered."
            )

        agent_request = self._request_factory.create(
            agent_name=context.agent,
            capability=context.capability,
            request=context.request,
        )

                
        try:
            response = await agent.execute(
                agent_request,
            )

            context.response = response
        except Exception as exc:
            raise RuntimeError(
                f"Runtime execution failed: {exc}"
            ) from exc

        return RuntimeResult(
            success=response.success,
            execution_id=context.execution_id,
            agent=context.agent,
            capability=context.capability,
            result=response.result,
            metadata=(
                response.metadata.model_dump()
                if response.metadata
                else {}
            ),
        )