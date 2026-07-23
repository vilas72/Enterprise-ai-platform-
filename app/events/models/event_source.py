"""
Event Sources.
"""

from __future__ import annotations

from enum import Enum


class EventSource(str, Enum):
    """
    Supported platform event source.
    """
    AGENT_RUNTIME = "AgentRuntime"
    WORKFLOW_ENGINE = "WorkflowEngine"
    WORKFLOW_EXECUTOR = "WorkflowExecutor"
    GATEWAY = "EnterpriseGateway"