"""
Enterprise Gateway exceptions.
"""

from __future__ import annotations


class GatewayError(Exception):
    """
    Base Gateway exception.
    """


class GatewayRegistrationError(GatewayError):
    """
    Agent registration failed.
    """


class AgentNotFoundError(GatewayError):
    """
    No matching agent found.
    """


class UnsupportedCapabilityError(GatewayError):
    """
    Capability is not supported by any registered agent.
    """


class GatewayAuthorizationError(GatewayError):
    """
    Governance authorization failed.
    """


class GatewayExecutionError(GatewayError):
    """
    Gateway execution failed.
    """