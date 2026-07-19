"""
Reflection Exceptions.
"""

from __future__ import annotations


class ReflectionException(Exception):
    """
    Base Reflection exception.
    """


class ReflectionExecutionException(
    ReflectionException,
):
    """
    Reflection execution failed.
    """


class ReflectionConfigurationException(
    ReflectionException,
):
    """
    Reflection configuration error.
    """