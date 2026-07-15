"""
Support Agent exceptions.
"""

from __future__ import annotations


class SupportAgentError(Exception):
    """
    Base exception for all Support Agent errors.
    """


class UnsupportedSupportCapabilityError(SupportAgentError):
    """
    Raised when an unsupported capability is requested.
    """


class TicketOperationError(SupportAgentError):
    """
    Raised when a ticket operation fails.
    """


class KnowledgeOperationError(SupportAgentError):
    """
    Raised when a knowledge operation fails.
    """


class IncidentAnalysisError(SupportAgentError):
    """
    Raised when incident analysis fails.
    """


class ResolutionGenerationError(SupportAgentError):
    """
    Raised when AI cannot generate a resolution.
    """