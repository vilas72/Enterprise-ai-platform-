"""
Runtime Exceptions.
"""

from __future__ import annotations


class RuntimeException(Exception):
    """
    Base runtime exception.
    """


class RuntimeExecutionException(
    RuntimeException,
):
    """
    Runtime execution failure.
    """


class RuntimeValidationException(
    RuntimeException,
):
    """
    Runtime validation failure.
    """


class RuntimeTimeoutException(
    RuntimeException,
):
    """
    Runtime timeout.
    """