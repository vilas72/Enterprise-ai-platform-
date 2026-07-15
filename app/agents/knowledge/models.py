"""
Knowledge Runtime domain models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class KnowledgeSource(str, Enum):
    """
    Supported enterprise knowledge sources.
    """

    INTERNAL = "internal"
    CONFLUENCE = "confluence"
    SHAREPOINT = "sharepoint"
    GITHUB = "github"
    JIRA = "jira"
    ALL = "all"


class KnowledgeRequest(BaseModel):
    """
    Enterprise knowledge request.
    """

    query: str = Field(..., min_length=1)

    source: KnowledgeSource = KnowledgeSource.ALL

    top_k: int = Field(default=5, ge=1, le=50)

    filters: dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """
    Single retrieved knowledge document.
    """

    id: str

    title: str

    content: str

    source: KnowledgeSource

    score: float

    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeResponse(BaseModel):
    """
    Knowledge response.
    """

    query: str

    answer: str | None = None

    results: list[SearchResult] = Field(default_factory=list)

    citations: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeCapability(str, Enum):
    """Knowledge Agent capabilities."""

    SEARCH = "search"
    ANSWER = "answer"
    SUMMARIZE = "summarize"
    RECOMMEND = "recommend"
    EXPLAIN = "explain"
    REWRITE = "rewrite"


class KnowledgeExecutionMetadata(BaseModel):
    """Execution metadata captured by Knowledge Agent."""

    governance_approved: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class KnowledgeAgentRequest(KnowledgeRequest):
    """Agent-facing knowledge request model."""

    capability: KnowledgeCapability


class KnowledgeAgentResponse(BaseModel):
    """Agent-facing knowledge response model."""

    success: bool
    capability: KnowledgeCapability
    message: str
    result: Any | None = None
    metadata: KnowledgeExecutionMetadata = Field(
        default_factory=KnowledgeExecutionMetadata
    )