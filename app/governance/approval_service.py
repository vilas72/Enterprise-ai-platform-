import asyncio

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.governance.models import (
    ApprovalRequest,
    ApprovalStatus,
)


class ApprovalService:
    """
    Manages governance approval requests.

    Responsibilities
    ----------------
    • Create approval requests
    • Approve requests
    • Reject requests
    • Query approvals
    • Maintain approval history

    Persistence is intentionally abstracted away. The current
    implementation stores requests in memory and can later be
    backed by a database without changing the public interface.
    """

    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    async def create_request(
        self,
        *,
        conversation_id: str,
        execution_id: str,
        requester: str,
        action: str,
        resource: str,
        metadata: dict | None = None,
    ) -> ApprovalRequest:
        """
        Creates a new approval request.
        """

        request = ApprovalRequest(
            approval_id=str(uuid4()),
            conversation_id=conversation_id,
            execution_id=execution_id,
            requester=requester,
            action=action,
            resource=resource,
            created_at=datetime.now(timezone.utc),
            metadata=metadata or {},
        )

        self._requests[request.approval_id] = request

        return request

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    async def get_request(
        self,
        approval_id: str,
    ) -> ApprovalRequest | None:
        """
        Returns an approval request.
        """

        return self._requests.get(approval_id)

    async def exists(
        self,
        approval_id: str,
    ) -> bool:
        """
        Returns True if the approval exists.
        """

        return approval_id in self._requests

    async def list_requests(
        self,
    ) -> list[ApprovalRequest]:
        """
        Returns all approval requests.
        """

        return sorted(
            self._requests.values(),
            key=lambda request: request.created_at,
            reverse=True,
        )

    async def list_pending(
        self,
    ) -> list[ApprovalRequest]:
        """
        Returns all pending approval requests.
        """

        return [
            request
            for request in self._requests.values()
            if request.status == ApprovalStatus.PENDING
        ]

    async def list_by_requester(
        self,
        requester: str,
    ) -> list[ApprovalRequest]:
        """
        Returns approvals created by a requester.
        """

        return [
            request
            for request in self._requests.values()
            if request.requester == requester
        ]

    async def list_by_execution(
        self,
        execution_id: str,
    ) -> list[ApprovalRequest]:
        """
        Returns approvals for an execution.
        """

        return [
            request
            for request in self._requests.values()
            if request.execution_id == execution_id
        ]
        
        # ------------------------------------------------------------------
    # Approval Actions
    # ------------------------------------------------------------------

    async def approve(
        self,
        approval_id: str,
        approver: str,
        comments: str | None = None,
    ) -> ApprovalRequest:
        """
        Approve a pending request.

        Raises
        ------
        ValueError
            If the request does not exist or is not pending.
        """

        request = await self._require_request(approval_id)

        if request.status != ApprovalStatus.PENDING:
            raise ValueError(
                f"Approval request '{approval_id}' is not pending."
            )

        request.status = ApprovalStatus.APPROVED
        request.approver = approver
        request.comments = comments
        request.approved_at = datetime.now(timezone.utc)

        return request

    async def reject(
        self,
        approval_id: str,
        approver: str,
        comments: str | None = None,
    ) -> ApprovalRequest:
        """
        Reject a pending request.
        """

        request = await self._require_request(approval_id)

        if request.status != ApprovalStatus.PENDING:
            raise ValueError(
                f"Approval request '{approval_id}' is not pending."
            )

        request.status = ApprovalStatus.REJECTED
        request.approver = approver
        request.comments = comments
        request.approved_at = datetime.now(timezone.utc)

        return request

    async def delete(
        self,
        approval_id: str,
    ) -> bool:
        """
        Delete an approval request.

        Returns
        -------
        True if the request existed.
        """

        return self._requests.pop(approval_id, None) is not None

    async def clear(
        self,
    ) -> None:
        """
        Remove all approval requests.
        """

        self._requests.clear()

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    async def count(self) -> int:
        """
        Total approval requests.
        """

        return len(self._requests)

    async def get_statistics(
        self,
    ) -> dict[str, int]:
        """
        Returns approval statistics.
        """

        pending = 0
        approved = 0
        rejected = 0

        for request in self._requests.values():

            if request.status == ApprovalStatus.PENDING:
                pending += 1

            elif request.status == ApprovalStatus.APPROVED:
                approved += 1

            elif request.status == ApprovalStatus.REJECTED:
                rejected += 1

        return {
            "total": len(self._requests),
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _require_request(
        self,
        approval_id: str,
    ) -> ApprovalRequest:
        """
        Returns an approval request or raises.

        Raises
        ------
        ValueError
            If the request does not exist.
        """

        request = await self.get_request(approval_id)

        if request is None:
            raise ValueError(
                f"Approval request '{approval_id}' was not found."
            )

        return request    