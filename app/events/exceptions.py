"""
Event Exceptions.
"""

from __future__ import annotations


class EventException(Exception):
    """
    Base Event exception.
    """


class EventRegistrationException(EventException):
    """
    Raised when event registration fails.
    """


class EventDispatchException(EventException):
    """
    Raised when event dispatch fails.
    """