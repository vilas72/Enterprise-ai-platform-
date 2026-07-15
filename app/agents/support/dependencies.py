"""
Support Agent dependency registration.
"""

from __future__ import annotations

from functools import lru_cache

from app.agents.developer.dependencies import (
    get_ai_actions,
    get_jira_actions,
)
from app.agents.knowledge.dependencies import get_knowledge_actions
from app.agents.support.support_actions import SupportActions
from app.agents.support.support_agent import SupportAgent


@lru_cache
def get_support_actions() -> SupportActions:
    """
    Create SupportActions.
    """

    return SupportActions(
        jira_actions=get_jira_actions(),
        knowledge_actions=get_knowledge_actions(),
        ai_actions=get_ai_actions(),
    )


@lru_cache
def get_support_agent() -> SupportAgent:
    """
    Create SupportAgent.
    """

    return SupportAgent(support_actions=get_support_actions())