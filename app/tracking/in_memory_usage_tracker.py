from threading import RLock

from app.tracking.usage_record import UsageRecord
from app.tracking.usage_tracker import UsageTracker


class InMemoryUsageTracker(UsageTracker):
    """
    Thread-safe in-memory implementation of UsageTracker.

    Intended for development and testing.
    """

    def __init__(self):
        self._records: list[UsageRecord] = []
        self._lock = RLock()

    def record(
        self,
        usage: UsageRecord,
    ) -> None:
        """
        Record one AI request.
        """

        with self._lock:
            self._records.append(usage)

    def get_all(self) -> list[UsageRecord]:
        """
        Return all recorded usage.
        """

        with self._lock:
            return self._records.copy()

    def clear(self) -> None:
        """
        Remove all usage records.
        """

        with self._lock:
            self._records.clear()

    def total_requests(self) -> int:
        """
        Return total number of requests.
        """

        with self._lock:
            return len(self._records)

    def total_prompt_tokens(self) -> int:
        """
        Return total prompt tokens.
        """

        with self._lock:
            return sum(
                record.prompt_tokens
                for record in self._records
            )

    def total_completion_tokens(self) -> int:
        """
        Return total completion tokens.
        """

        with self._lock:
            return sum(
                record.completion_tokens
                for record in self._records
            )

    def total_tokens(self) -> int:
        """
        Return total tokens.
        """

        with self._lock:
            return sum(
                record.total_tokens
                for record in self._records
            )

    def total_cost(self) -> float:
        """
        Return accumulated estimated cost.
        """

        with self._lock:
            return round(
                sum(
                    record.estimated_cost
                    for record in self._records
                ),
                6,
            )

    def average_latency(self) -> float:
        """
        Return average request latency.
        """

        with self._lock:

            if not self._records:
                return 0.0

            return round(
                sum(
                    record.latency_ms
                    for record in self._records
                )
                / len(self._records),
                2,
            )
            
    def track(self, usage: UsageRecord) -> None:
        """
        Track one AI request.
        """

        self.record(usage)