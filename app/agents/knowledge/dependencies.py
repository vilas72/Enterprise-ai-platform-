"""
Dependency registration for the Knowledge Agent.
"""

from __future__ import annotations

from functools import lru_cache

from app.agents.knowledge.ai_actions import AIActions
from app.actions.knowledge_actions import KnowledgeActions
from app.agents.knowledge.knowledge_agent import KnowledgeAgent
from app.dependencies.service_dependencies import get_ai_service
from app.knowledge.runtime.dependencies import get_knowledge_runtime


@lru_cache
def get_ai_actions() -> AIActions:
    """Create AI actions."""
    return AIActions(ai_service=get_ai_service())


@lru_cache
def get_knowledge_actions() -> KnowledgeActions:
    """Create Knowledge actions."""
    return KnowledgeActions(knowledge_runtime=get_knowledge_runtime())


@lru_cache
def get_knowledge_agent() -> KnowledgeAgent:
    """Create the Knowledge Agent."""
    return KnowledgeAgent(
        knowledge_actions=get_knowledge_actions(),
        ai_actions=get_ai_actions(),
    )
