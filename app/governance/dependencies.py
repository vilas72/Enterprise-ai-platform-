from __future__ import annotations

from functools import lru_cache

from app.governance.approval_service import ApprovalService
from app.governance.audit_service import AuditService
from app.governance.compliance_service import ComplianceService
from app.governance.governance_runtime import GovernanceRuntime
from app.governance.policy_service import PolicyService


@lru_cache(maxsize=1)
def get_policy_service() -> PolicyService:
    """
    Returns the singleton PolicyService.
    """

    return PolicyService()


@lru_cache(maxsize=1)
def get_approval_service() -> ApprovalService:
    """
    Returns the singleton ApprovalService.
    """

    return ApprovalService()


@lru_cache(maxsize=1)
def get_audit_service() -> AuditService:
    """
    Returns the singleton AuditService.
    """

    return AuditService()


@lru_cache(maxsize=1)
def get_compliance_service() -> ComplianceService:
    """
    Returns the singleton ComplianceService.
    """

    return ComplianceService()


@lru_cache(maxsize=1)
def get_governance_runtime() -> GovernanceRuntime:
    """
    Returns the singleton GovernanceRuntime.
    """

    return GovernanceRuntime(
        policy_service=get_policy_service(),
        approval_service=get_approval_service(),
        audit_service=get_audit_service(),
        compliance_service=get_compliance_service(),
    )