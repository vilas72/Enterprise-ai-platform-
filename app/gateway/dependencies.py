"""
Enterprise Gateway dependency registration.
"""

from __future__ import annotations

from functools import lru_cache

from app.agents.developer.dependencies import get_developer_agent
from app.agents.knowledge.dependencies import get_knowledge_agent
from app.agents.support.dependencies import get_support_agent
from app.agents.devops.dependencies import get_devops_agent

from app.agents.planner.planner import Planner
from app.agents.planner.planner_registry import PlannerRegistry
from app.agents.planner.planner_types import PlannerType

from app.gateway.gateway import EnterpriseGateway
from app.gateway.registry import GatewayRegistry
from app.gateway.router import GatewayRouter

from app.workflow.workflow_builder import WorkflowBuilder
from app.workflow.workflow_executor import WorkflowExecutor
from app.workflow.workflow_engine import WorkflowEngine

from app.runtime.agent_runtime import AgentRuntime
from app.runtime.runtime_executor import RuntimeExecutor
from app.events.dependencies import get_event_publisher


@lru_cache
def get_gateway_registry() -> GatewayRegistry:
    """
    Create and populate the gateway registry.
    """

    registry = GatewayRegistry()

    registry.register(
        "developer",
        get_developer_agent(),
    )

    registry.register(
        "knowledge",
        get_knowledge_agent(),
    )

    registry.register(
        "support",
        get_support_agent(),
    )

    registry.register(
        "devops",
        get_devops_agent(),
    )

    return registry


@lru_cache
def get_planner() -> Planner:
    """
    Create the Enterprise Planner.
    """

    registry = PlannerRegistry()

    return registry.get(
        PlannerType.RULE_BASED,
    )


@lru_cache
def get_gateway_router() -> GatewayRouter:
    """
    Create the Enterprise Gateway Router.
    """

    return GatewayRouter(
        registry=get_gateway_registry(),
    )


@lru_cache
def get_workflow_builder() -> WorkflowBuilder:
    """
    Create the Workflow Builder.
    """

    return WorkflowBuilder()

@lru_cache
def get_workflow_executor() -> WorkflowExecutor:
    """
    Create the Workflow Executor.
    """

    return WorkflowExecutor(
        runtime=get_agent_runtime(),
        publisher=get_event_publisher(),
    )

@lru_cache
def get_workflow_engine() -> WorkflowEngine:

    return WorkflowEngine(
        executor=get_workflow_executor(),
        publisher=get_event_publisher(),
    )
    
@lru_cache
def get_runtime_executor() -> RuntimeExecutor:
    """
    Create the Runtime Executor.
    """

    return RuntimeExecutor(
        router=get_gateway_router(),
    )
    
@lru_cache
def get_agent_runtime() -> AgentRuntime:
    """
    Create the Agent Runtime.
    """

    return AgentRuntime(
        executor=get_runtime_executor(),
        publisher=get_event_publisher(),
    )
    
   
    
@lru_cache
def get_enterprise_gateway() -> EnterpriseGateway:
    """
    Create the Enterprise Gateway.
    """

    return EnterpriseGateway(
        planner=get_planner(),
        router=get_gateway_router(),
        workflow_builder=get_workflow_builder(),
        workflow_engine=get_workflow_engine(),
        publisher=get_event_publisher(),
    )