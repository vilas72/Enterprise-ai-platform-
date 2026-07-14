from enum import Enum


class GoalPriority(str, Enum):
    """
    Business priority of a goal.
    """

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"