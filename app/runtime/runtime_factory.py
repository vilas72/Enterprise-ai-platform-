"""
Runtime Factory.
"""

from __future__ import annotations

from app.gateway.router import GatewayRouter
from app.runtime.agent_runtime import AgentRuntime
from app.runtime.runtime_executor import RuntimeExecutor


class RuntimeFactory:
    """
    Creates runtime instances.
    """

    @staticmethod
    def create(
        router: GatewayRouter,
    ) -> AgentRuntime:
        """
        Create the Agent Runtime.
        """

        executor = RuntimeExecutor(
            router=router,
        )

        return AgentRuntime(
            executor=executor,
        )