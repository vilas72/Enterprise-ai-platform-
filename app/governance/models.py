from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class PolicyEffect(str, Enum):
    """
    Defines the outcome of a policy evaluation.
    """

    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class ApprovalStatus(str, Enum):
    """
    Approval workflow status.
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AuditSeverity(str, Enum):
    """
    Audit event severity.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(slots=True)
class PolicyDecision:
    """
    Result of evaluating a governance policy.
    """

    allowed: bool

    effect: PolicyEffect

    reason: str | None = None

    policy_name: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ApprovalRequest:
    """
    Represents a request requiring human approval.
    """

    approval_id: str

    conversation_id: str

    execution_id: str

    requester: str

    action: str

    resource: str

    created_at: datetime

    status: ApprovalStatus = ApprovalStatus.PENDING

    approver: str | None = None

    approved_at: datetime | None = None

    comments: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditRecord:
    """
    Immutable audit log entry.
    """

    audit_id: str

    timestamp: datetime

    component: str

    action: str

    severity: AuditSeverity

    conversation_id: str | None = None

    execution_id: str | None = None

    actor: str | None = None

    outcome: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ComplianceResult:
    """
    Result of compliance validation.
    """

    compliant: bool

    violations: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)