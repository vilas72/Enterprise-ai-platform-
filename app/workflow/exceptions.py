"""
Workflow Exceptions.
"""

from __future__ import annotations


class WorkflowException(Exception):
    """
    Base workflow exception.
    """


class WorkflowExecutionException(WorkflowException):
    """
    Raised when workflow execution fails.
    """


class WorkflowValidationException(WorkflowException):
    """
    Raised when workflow validation fails.
    """


class WorkflowNotFoundException(WorkflowException):
    """
    Raised when workflow cannot be found.
    """