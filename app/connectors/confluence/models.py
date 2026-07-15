"""
Enterprise Confluence domain models.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ConfluenceContentType(str, Enum):
    """
    Supported Confluence content types.
    """

    PAGE = "page"
    BLOGPOST = "blogpost"
    ATTACHMENT = "attachment"
    COMMENT = "comment"


class ConfluencePageStatus(str, Enum):
    """
    Page lifecycle status.
    """

    CURRENT = "current"
    DRAFT = "draft"
    ARCHIVED = "archived"
    TRASHED = "trashed"


class ConfluenceSpace(BaseModel):
    """
    Confluence space.
    """

    id: str

    key: str

    name: str

    type: str | None = None

    description: str | None = None

    homepage_id: str | None = None

    web_url: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ConfluenceVersion(BaseModel):
    """
    Version information.
    """

    number: int

    author: str | None = None

    created_at: datetime | None = None

    message: str | None = None


class ConfluenceLabel(BaseModel):
    """
    Page label.
    """

    id: str | None = None

    name: str

    prefix: str | None = None


class ConfluenceAttachment(BaseModel):
    """
    Page attachment.
    """

    id: str

    title: str

    media_type: str | None = None

    file_size: int | None = None

    download_url: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ConfluencePage(BaseModel):
    """
    Enterprise Confluence page.
    """

    id: str

    title: str

    type: ConfluenceContentType = (
        ConfluenceContentType.PAGE
    )

    status: ConfluencePageStatus = (
        ConfluencePageStatus.CURRENT
    )

    space_key: str

    space_name: str | None = None

    parent_id: str | None = None

    version: ConfluenceVersion | None = None

    body: str | None = None

    web_url: str | None = None

    created_at: datetime | None = None

    updated_at: datetime | None = None

    labels: list[ConfluenceLabel] = Field(
        default_factory=list,
    )

    attachments: list[ConfluenceAttachment] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ConfluenceSearchResult(BaseModel):
    """
    Search result.
    """

    page: ConfluencePage

    score: float | None = None

    excerpt: str | None = None


class ConfluenceSearchResponse(BaseModel):
    """
    Enterprise search response.
    """

    query: str

    total: int

    results: list[ConfluenceSearchResult] = Field(
        default_factory=list,
    )


class ConfluencePageSummary(BaseModel):
    """
    Lightweight page summary.
    """

    id: str

    title: str

    space_key: str

    web_url: str | None = None


class ConfluenceSpaceSummary(BaseModel):
    """
    Lightweight space summary.
    """

    id: str

    key: str

    name: str


class ConfluencePageTree(BaseModel):
    """
    Parent-child page hierarchy.
    """

    page: ConfluencePageSummary

    children: list["ConfluencePageTree"] = Field(
        default_factory=list,
    )


ConfluencePageTree.model_rebuild()