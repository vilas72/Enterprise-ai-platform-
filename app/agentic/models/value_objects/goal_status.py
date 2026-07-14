from enum import Enum


class GoalStatus(str, Enum):
    """
    Lifecycle states of an enterprise goal.
    """

    CREATED = "created"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    REPLANNING = "replanning"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"