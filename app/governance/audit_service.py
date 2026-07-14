from __future__ import annotations

import asyncio

from datetime import datetime, timezone
from uuid import uuid4

from app.governance.models import (
    AuditRecord,
    AuditSeverity,
)


class AuditService:
    """
    Records immutable governance audit events.

    Responsibilities
    ----------------
    • Record audit events
    • Search audit history
    • Filter by conversation
    • Filter by execution
    • Filter by component
    • Filter by severity

    The current implementation stores audit records in memory.
    The public interface is intentionally persistence-agnostic,
    allowing future database integration without changing callers.
    """

    def __init__(self) -> None:

        self._records: list[AuditRecord] = []
        
        self._record_index: dict[str, AuditRecord] = {}

        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    async def record(
        self,
        *,
        component: str,
        action: str,
        severity: AuditSeverity,
        conversation_id: str | None = None,
        execution_id: str | None = None,
        actor: str | None = None,
        outcome: str | None = None,
        metadata: dict | None = None,
    ) -> AuditRecord:
        """
        Record an immutable audit event.
        """

        record = AuditRecord(
            audit_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc),
            component=component,
            action=action,
            severity=severity,
            conversation_id=conversation_id,
            execution_id=execution_id,
            actor=actor,
            outcome=outcome,
            metadata=metadata or {},
        )

        async with self._lock:
            self._records.append(record)
            self._record_index[record.audit_id] = record

        return record

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    async def get(
        self,
        audit_id: str,
    ) -> AuditRecord | None:
        """
        Returns an audit record.
        """

        async with self._lock:

            for record in self._records:
                if record.audit_id == audit_id:
                    return record

        return None

    async def list_records(
        self,
    ) -> list[AuditRecord]:
        """
        Returns all audit records.
        """

        async with self._lock:
            return list(self._records)

    async def list_by_conversation(
        self,
        conversation_id: str,
    ) -> list[AuditRecord]:
        """
        Returns all audit records for a conversation.
        """

        async with self._lock:

            return [
                record
                for record in self._records
                if record.conversation_id == conversation_id
            ]

    async def list_by_execution(
        self,
        execution_id: str,
    ) -> list[AuditRecord]:
        """
        Returns all audit records for an execution.
        """

        async with self._lock:

            return [
                record
                for record in self._records
                if record.execution_id == execution_id
            ]
            
        # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    async def list_by_component(
        self,
        component: str,
    ) -> list[AuditRecord]:
        """
        Returns all audit records for a component.
        """

        async with self._lock:
            return [
                record
                for record in self._records
                if record.component == component
            ]

    async def list_by_actor(
        self,
        actor: str,
    ) -> list[AuditRecord]:
        """
        Returns all audit records for an actor.
        """

        async with self._lock:
            return [
                record
                for record in self._records
                if record.actor == actor
            ]

    async def list_by_severity(
        self,
        severity: AuditSeverity,
    ) -> list[AuditRecord]:
        """
        Returns all audit records with the specified severity.
        """

        async with self._lock:
            return [
                record
                for record in self._records
                if record.severity == severity
            ]

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    async def search(
        self,
        *,
        component: str | None = None,
        actor: str | None = None,
        severity: AuditSeverity | None = None,
        conversation_id: str | None = None,
        execution_id: str | None = None,
        action: str | None = None,
    ) -> list[AuditRecord]:
        """
        Search audit records using one or more filters.
        """

        async with self._lock:
            records = list(self._records)

        if component is not None:
            records = [
                record
                for record in records
                if record.component == component
            ]

        if actor is not None:
            records = [
                record
                for record in records
                if record.actor == actor
            ]

        if severity is not None:
            records = [
                record
                for record in records
                if record.severity == severity
            ]

        if conversation_id is not None:
            records = [
                record
                for record in records
                if record.conversation_id == conversation_id
            ]

        if execution_id is not None:
            records = [
                record
                for record in records
                if record.execution_id == execution_id
            ]

        if action is not None:
            records = [
                record
                for record in records
                if record.action == action
            ]

        return records

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    async def count(
        self,
    ) -> int:
        """
        Returns the total number of audit records.
        """

        async with self._lock:
            return len(self._records)

    async def get_statistics(
        self,
    ) -> dict[str, int]:
        """
        Returns audit statistics grouped by severity.
        """

        async with self._lock:
            records = list(self._records)

        statistics = {
            "total": len(records),
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
        }

        for record in records:
            statistics[record.severity.value] += 1

        return statistics

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    async def purge_before(
        self,
        timestamp: datetime,
    ) -> int:
        """
        Removes audit records older than the supplied timestamp.

        Returns
        -------
        Number of deleted records.
        """

        async with self._lock:
            before = len(self._records)

            self._records = [
                record
                for record in self._records
                if record.timestamp >= timestamp
            ]

            return before - len(self._records)

    async def clear(
        self,
    ) -> None:
        """
        Removes all audit records.
        """

        async with self._lock:
            self._records.clear()