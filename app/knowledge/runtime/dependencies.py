"""
Knowledge Runtime dependency registration.
"""

from __future__ import annotations

from functools import lru_cache

from app.dependencies.service_dependencies import get_ai_service
from app.knowledge.retrieval.hybrid_search import HybridSearch
from app.knowledge.runtime.knowledge_runtime import KnowledgeRuntime


@lru_cache
def get_hybrid_search() -> HybridSearch:
    """Build the singleton hybrid search service."""
    return HybridSearch(search_providers=[])


@lru_cache
def get_knowledge_runtime() -> KnowledgeRuntime:
    """Build the singleton Knowledge Runtime."""
    return KnowledgeRuntime(
        ai_service=get_ai_service(),
        hybrid_search=get_hybrid_search(),
    )
