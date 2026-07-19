"""
Event Types.
"""

from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    """
    Supported platform event types.
    """

    # Gateway
    GATEWAY_STARTED = "gateway.started"
    GATEWAY_COMPLETED = "gateway.completed"
    GATEWAY_FAILED = "gateway.failed"

    # Planner
    PLANNER_STARTED = "planner.started"
    PLANNER_COMPLETED = "planner.completed"
    PLANNER_FAILED = "planner.failed"

    # Workflow
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"

    # Workflow Step
    STEP_STARTED = "workflow.step.started"
    STEP_COMPLETED = "workflow.step.completed"
    STEP_FAILED = "workflow.step.failed"

    # Runtime
    RUNTIME_STARTED = "runtime.started"
    RUNTIME_COMPLETED = "runtime.completed"
    RUNTIME_FAILED = "runtime.failed"

    # Agent
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"

    # Reflection
    REFLECTION_STARTED = "reflection.started"
    REFLECTION_COMPLETED = "reflection.completed"
    REFLECTION_FAILED = "reflection.failed"

    # Governance
    GOVERNANCE_STARTED = "governance.started"
    GOVERNANCE_COMPLETED = "governance.completed"
    GOVERNANCE_FAILED = "governance.failed"

    # Audit
    AUDIT_CREATED = "audit.created"

    # System
    SYSTEM_ERROR = "system.error"