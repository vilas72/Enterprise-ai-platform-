from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class GitHubIssueState(str, Enum):
    """
    GitHub issue state.
    """

    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"


class GitHubPullRequestState(str, Enum):
    """
    GitHub pull request state.
    """

    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"
    ALL = "all"


@dataclass(slots=True)
class GitHubRepository:
    """
    GitHub repository metadata.
    """

    id: int

    name: str

    full_name: str

    owner: str

    private: bool

    default_branch: str

    description: str | None = None

    clone_url: str | None = None

    html_url: str | None = None

    language: str | None = None


@dataclass(slots=True)
class GitHubIssue:
    """
    GitHub issue.
    """

    id: int

    number: int

    title: str

    state: GitHubIssueState

    repository: str

    author: str

    created_at: datetime

    updated_at: datetime

    body: str | None = None

    assignee: str | None = None

    labels: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GitHubPullRequest:
    """
    GitHub pull request.
    """

    id: int

    number: int

    repository: str

    title: str

    state: GitHubPullRequestState

    author: str

    source_branch: str

    target_branch: str

    created_at: datetime

    updated_at: datetime

    merged: bool = False

    mergeable: bool | None = None

    reviewers: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GitHubCommit:
    """
    GitHub commit.
    """

    sha: str

    message: str

    author: str

    timestamp: datetime

    url: str | None = None


@dataclass(slots=True)
class GitHubWorkflowRun:
    """
    GitHub Actions workflow execution.
    """

    id: int

    name: str

    status: str

    conclusion: str | None

    branch: str

    commit_sha: str

    created_at: datetime

    updated_at: datetime

    html_url: str | None = None