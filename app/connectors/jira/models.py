from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class JiraIssueType(str, Enum):
    """
    Supported Jira issue types.
    """

    TASK = "Task"
    BUG = "Bug"
    STORY = "Story"
    EPIC = "Epic"
    SUB_TASK = "Sub-task"


class JiraIssueStatus(str, Enum):
    """
    Common Jira workflow statuses.
    """

    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class JiraPriority(str, Enum):
    """
    Common Jira priorities.
    """

    LOWEST = "Lowest"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    HIGHEST = "Highest"


@dataclass(slots=True)
class JiraProject:
    """
    Jira project metadata.
    """

    id: str
    key: str
    name: str
    project_type: str
    url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class JiraIssue:
    """
    Jira issue.
    """

    id: str
    key: str

    project_key: str

    summary: str

    description: str | None

    issue_type: JiraIssueType

    status: JiraIssueStatus

    priority: JiraPriority | None

    assignee: str | None

    reporter: str | None

    created_at: datetime

    updated_at: datetime

    labels: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class JiraComment:
    """
    Jira issue comment.
    """

    id: str

    author: str

    body: str

    created_at: datetime

    updated_at: datetime

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class JiraSprint:
    """
    Jira sprint.
    """

    id: int

    name: str

    state: str

    start_date: datetime | None

    end_date: datetime | None

    goal: str | None

    metadata: dict[str, Any] = field(default_factory=dict)