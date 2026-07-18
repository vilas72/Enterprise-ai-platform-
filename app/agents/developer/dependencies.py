"""
Dependency providers for the Enterprise Developer Agent.
"""

from __future__ import annotations

from functools import lru_cache

from app.actions.ai_actions import AIActions
from app.agents.developer.developer_agent import DeveloperAgent
from app.actions.github_actions import GitHubActions
from app.actions.jira_actions import JiraActions

from app.connectors.github.dependencies import (
    get_github_connector,
)
from app.connectors.jira.dependencies import (
    get_jira_connector,
)

from app.services.ai_service import AIService
from app.dependencies.service_dependencies import (
    get_ai_service,
)


def get_github_actions() -> GitHubActions:
    """
    Return GitHubActions singleton.
    """
    return GitHubActions(
        github_connector=get_github_connector(),
    )


@lru_cache
def get_jira_actions() -> JiraActions:
    """
    Return JiraActions singleton.
    """
    return JiraActions(
        jira_connector=get_jira_connector(),
    )


@lru_cache
def get_ai_actions() -> AIActions:
    """
    Return AIActions singleton.
    """
    ai_service: AIService = get_ai_service()

    return AIActions(
        ai_service=ai_service,
    )


def get_developer_agent() -> DeveloperAgent:
    """
    Return DeveloperAgent singleton.
    """

    return DeveloperAgent(
        github_actions=get_github_actions(),
        jira_actions=get_jira_actions(),
        ai_actions=get_ai_actions(),
    )
