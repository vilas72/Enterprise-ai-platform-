"""
Runtime Dependency Providers.

Owns all Runtime layer singletons.

Dependency Graph

GatewayRouter
      │
      ▼
RuntimeExecutor
      │
      ▼
AgentRuntime
"""

from __future__ import annotations

from functools import lru_cache

from app.events.dependencies import get_event_publisher

from app.gateway.dependencies import (
    get_gateway_router,
)

from app.runtime.agent_runtime import (
    AgentRuntime,
)

from app.runtime.runtime_executor import (
    RuntimeExecutor,
)


@lru_cache
def get_runtime_executor() -> RuntimeExecutor:
    """
    Return the shared RuntimeExecutor.
    """

    return RuntimeExecutor(
        router=get_gateway_router(),
    )


@lru_cache
def get_agent_runtime() -> AgentRuntime:
    """
    Return the shared AgentRuntime.
    """

    return AgentRuntime(
        executor=get_runtime_executor(),
        publisher=get_event_publisher(),
    )