"""
Enterprise DevOps Agent exceptions.
"""

from __future__ import annotations


class DevOpsAgentError(Exception):
    """
    Base DevOps Agent exception.
    """


class UnsupportedCapabilityError(DevOpsAgentError):
    """
    Unsupported DevOps capability.
    """


class RepositoryAnalysisError(DevOpsAgentError):
    """
    Repository analysis failed.
    """


class PullRequestAnalysisError(DevOpsAgentError):
    """
    Pull request analysis failed.
    """


class BuildAnalysisError(DevOpsAgentError):
    """
    Build analysis failed.
    """


class DeploymentAnalysisError(DevOpsAgentError):
    """
    Deployment analysis failed.
    """


class IncidentAnalysisError(DevOpsAgentError):
    """
    Incident analysis failed.
    """


class RunbookGenerationError(DevOpsAgentError):
    """
    Runbook generation failed.
    """