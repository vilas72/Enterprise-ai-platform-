"""
Developer Agent exceptions.
"""

from __future__ import annotations


class DeveloperAgentException(Exception):
    """
    Base exception for Developer Agent.
    """


class DeveloperValidationException(
    DeveloperAgentException,
):
    """
    Invalid developer request.
    """


class UnsupportedCapabilityException(
    DeveloperAgentException,
):
    """
    Unsupported developer capability.
    """


class RepositoryNotFoundException(
    DeveloperAgentException,
):
    """
    Repository not found.
    """


class PullRequestException(
    DeveloperAgentException,
):
    """
    Pull request operation failed.
    """


class GitHubOperationException(
    DeveloperAgentException,
):
    """
    GitHub operation failed.
    """


class JiraOperationException(
    DeveloperAgentException,
):
    """
    Jira operation failed.
    """


class CodeGenerationException(
    DeveloperAgentException,
):
    """
    AI code generation failed.
    """


class DocumentationGenerationException(
    DeveloperAgentException,
):
    """
    Documentation generation failed.
    """


class ArchitectureAnalysisException(
    DeveloperAgentException,
):
    """
    Architecture analysis failed.
    """