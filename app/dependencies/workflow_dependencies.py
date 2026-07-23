"""
Workflow dependency registration.

This module owns Runtime and Workflow object creation.
It intentionally does NOT create AI services, which belong in
service_dependencies.py.
"""

from __future__ import annotations

from functools import lru_cache

from app.bootstrap.workflow_bootstrap import (
    get_workflow_builder,
    get_workflow_registry,
    get_workflow_hook_manager,
)

from app.events.dependencies import get_event_publisher

from app.runtime.runtime_executor import RuntimeExecutor
from app.runtime.agent_runtime import AgentRuntime

from app.dependencies.gateway_registry_dependencies import (
    get_gateway_registry,
)
from app.workflow.workflow_engine import WorkflowEngine
from app.workflow.workflow_executor import WorkflowExecutor
from app.workflow.workflow_service import WorkflowService

from app.dependencies.planner_dependencies import get_planner

#
# Runtime
#

_runtime_executor = RuntimeExecutor(
    registry=get_gateway_registry(),
)

_agent_runtime = AgentRuntime(
    executor=_runtime_executor,
    publisher=get_event_publisher(),
)


#
# Workflow
#

_workflow_executor = WorkflowExecutor(
    runtime=_agent_runtime,
    publisher=get_event_publisher(),
    hooks=get_workflow_hook_manager(),
)

_workflow_engine = WorkflowEngine(
    executor=_workflow_executor,
    publisher=get_event_publisher(),
    hooks=get_workflow_hook_manager(),
)

_workflow_service = WorkflowService(
    planner=get_planner(),
    builder=get_workflow_builder(),
    registry=get_workflow_registry(),
    engine=_workflow_engine,
)


#
# Providers
#

@lru_cache
def get_runtime_executor() -> RuntimeExecutor:
    return _runtime_executor


@lru_cache
def get_agent_runtime() -> AgentRuntime:
    return _agent_runtime


@lru_cache
def get_workflow_executor() -> WorkflowExecutor:
    return _workflow_executor


@lru_cache
def get_workflow_engine() -> WorkflowEngine:
    return _workflow_engine


@lru_cache
def get_workflow_service() -> WorkflowService:
    return _workflow_service