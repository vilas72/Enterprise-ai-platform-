from abc import ABC, abstractmethod

from app.tracking.usage_record import UsageRecord


class UsageTracker(ABC):
    """
    Abstract usage tracker.

    Responsible for recording and retrieving
    AI usage statistics.
    """

    @abstractmethod
    def record(
        self,
        usage: UsageRecord,
    ) -> None:
        """
        Record one AI request.
        """
        pass

    @abstractmethod
    def get_all(self) -> list[UsageRecord]:
        """
        Return all usage records.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all usage records.
        """
        pass

    @abstractmethod
    def total_requests(self) -> int:
        """
        Return total number of requests.
        """
        pass