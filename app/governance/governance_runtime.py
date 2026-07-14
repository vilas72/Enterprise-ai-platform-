from __future__ import annotations

from typing import Any

from app.governance.approval_service import ApprovalService
from app.governance.audit_service import AuditService
from app.governance.compliance_service import ComplianceService
from app.governance.models import (
    ApprovalRequest,
    AuditSeverity,
    ComplianceResult,
    PolicyDecision,
    PolicyEffect,
)
from app.governance.policy_service import PolicyService


class GovernanceRuntime:
    """
    Enterprise Governance Runtime.

    Coordinates:

    • Policy evaluation
    • Compliance validation
    • Approval workflow
    • Audit logging

    This runtime is intended to be invoked before executing
    AI requests, Tool executions, Connector operations and
    Agent actions.
    """

    def __init__(
        self,
        policy_service: PolicyService,
        approval_service: ApprovalService,
        audit_service: AuditService,
        compliance_service: ComplianceService,
    ) -> None:
        self._policy_service = policy_service
        self._approval_service = approval_service
        self._audit_service = audit_service
        self._compliance_service = compliance_service

    # ------------------------------------------------------------------
    # Authorization
    # ------------------------------------------------------------------

    async def authorize(
        self,
        *,
        component: str,
        operation: str,
        resource: str,
        metadata: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """
        Evaluate governance policies.
        """

        return await self._policy_service.evaluate(
            component=component,
            operation=operation,
            resource=resource,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # Compliance
    # ------------------------------------------------------------------

    async def validate(
        self,
        *,
        context: dict[str, Any],
    ) -> ComplianceResult:
        """
        Execute compliance validation.
        """

        return await self._compliance_service.validate(
            context=context,
        )

    # ------------------------------------------------------------------
    # Approval
    # ------------------------------------------------------------------

    async def request_approval(
        self,
        *,
        conversation_id: str,
        execution_id: str,
        requester: str,
        action: str,
        resource: str,
        metadata: dict[str, Any] | None = None,
    ) -> ApprovalRequest:
        """
        Create a governance approval request.
        """

        return await self._approval_service.create_request(
            conversation_id=conversation_id,
            execution_id=execution_id,
            requester=requester,
            action=action,
            resource=resource,
            metadata=metadata,
        )

    async def approve(
        self,
        approval_id: str,
        approver: str,
        comments: str | None = None,
    ) -> ApprovalRequest:
        """
        Approve a governance request.
        """

        return await self._approval_service.approve(
            approval_id=approval_id,
            approver=approver,
            comments=comments,
        )

    async def reject(
        self,
        approval_id: str,
        approver: str,
        comments: str | None = None,
    ) -> ApprovalRequest:
        """
        Reject a governance request.
        """

        return await self._approval_service.reject(
            approval_id=approval_id,
            approver=approver,
            comments=comments,
        )

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    async def audit(
        self,
        *,
        component: str,
        action: str,
        severity: AuditSeverity,
        conversation_id: str | None = None,
        execution_id: str | None = None,
        actor: str | None = None,
        outcome: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Record an audit event.
        """

        await self._audit_service.record(
            component=component,
            action=action,
            severity=severity,
            conversation_id=conversation_id,
            execution_id=execution_id,
            actor=actor,
            outcome=outcome,
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # End-to-End Governance
    # ------------------------------------------------------------------

    async def evaluate_request(
        self,
        *,
        component: str,
        operation: str,
        resource: str,
        context: dict[str, Any],
        conversation_id: str,
        execution_id: str,
        requester: str,
    ) -> tuple[
        PolicyDecision,
        ComplianceResult,
        ApprovalRequest | None,
    ]:
        """
        Execute the complete governance workflow.

        Steps:
        1. Policy evaluation
        2. Compliance validation
        3. Approval creation (if required)
        """

        decision = await self.authorize(
            component=component,
            operation=operation,
            resource=resource,
            metadata=context,
        )

        compliance = await self.validate(
            context=context,
        )

        approval = None

        if decision.effect == PolicyEffect.REQUIRE_APPROVAL:
            approval = await self.request_approval(
                conversation_id=conversation_id,
                execution_id=execution_id,
                requester=requester,
                action=operation,
                resource=resource,
                metadata=context,
            )

        return (
            decision,
            compliance,
            approval,
        )