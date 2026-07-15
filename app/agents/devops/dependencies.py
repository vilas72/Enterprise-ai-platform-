"""
Dependency registration for the Enterprise DevOps Agent.
"""

from __future__ import annotations

from functools import lru_cache

from app.agents.developer.dependencies import (
    get_ai_actions,
    get_github_actions,
    get_jira_actions,
)
from app.agents.knowledge.dependencies import get_knowledge_actions
from app.agents.devops.devops_actions import DevOpsActions
from app.agents.devops.devops_agent import DevOpsAgent


@lru_cache
def get_devops_actions() -> DevOpsActions:
    """
    Create the Enterprise DevOps business actions.
    """

    return DevOpsActions(
        github_actions=get_github_actions(),
        jira_actions=get_jira_actions(),
        knowledge_actions=get_knowledge_actions(),
        ai_actions=get_ai_actions(),
    )


@lru_cache
def get_devops_agent() -> DevOpsAgent:
    """
    Create the Enterprise DevOps Agent.
    """

    return DevOpsAgent(devops_actions=get_devops_actions())