"""Tool domain models — the core vocabulary for the tool execution system."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolStatus(str, Enum):
    """Execution status of a tool call."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    PERMISSION_DENIED = "permission_denied"
    NOT_FOUND = "not_found"


@dataclass(frozen=True)
class ToolParameter:
    """
    Describes a single input parameter for a tool.

    Attributes:
        name: Parameter name (used as dict key in ToolInput)
        type: Python type hint string (e.g. "str", "int", "list[str]")
        description: Human-readable description for LLM prompt generation
        required: Whether the parameter must be provided
        default: Default value when required=False
    """

    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


@dataclass(frozen=True)
class ToolMetadata:
    """
    Static metadata describing a tool's identity and interface.

    Attributes:
        name: Unique tool name (snake_case)
        description: LLM-facing description used in prompt generation
        parameters: Ordered list of input parameter definitions
        tags: Optional classification tags (e.g. ["math", "safe"])
        version: Semantic version string
    """

    name: str
    description: str
    parameters: tuple[ToolParameter, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    version: str = "1.0.0"


@dataclass(frozen=True)
class ToolInput:
    """
    Immutable input payload for a tool invocation.

    Attributes:
        tool_name: Name of the tool to invoke
        parameters: Key-value arguments matching ToolMetadata.parameters
        call_id: Optional correlation ID for tracing
    """

    tool_name: str
    parameters: dict[str, Any]
    call_id: str = ""

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a parameter value by name."""
        return self.parameters.get(key, default)

    def require(self, key: str) -> Any:
        """
        Retrieve a required parameter value by name.

        Raises:
            KeyError: If the key is not present in parameters
        """
        if key not in self.parameters:
            raise KeyError(
                f"Required parameter '{key}' missing from ToolInput "
                f"for tool '{self.tool_name}'. "
                f"Available: {list(self.parameters.keys())}"
            )
        return self.parameters[key]


@dataclass(frozen=True)
class ToolOutput:
    """
    Immutable result of a tool execution.

    Attributes:
        tool_name: Name of the tool that produced this output
        status: Execution outcome
        result: Return value (None on error)
        error: Error message (None on success)
        call_id: Correlation ID echoed from ToolInput
        execution_time_ms: Wall-clock execution time
        metadata: Optional extra information from the tool
    """

    tool_name: str
    status: ToolStatus
    result: Any = None
    error: str | None = None
    call_id: str = ""
    execution_time_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status == ToolStatus.SUCCESS

    @property
    def is_error(self) -> bool:
        return self.status != ToolStatus.SUCCESS

    @classmethod
    def success(
        cls,
        tool_name: str,
        result: Any,
        call_id: str = "",
        execution_time_ms: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> "ToolOutput":
        """Factory for successful outputs."""
        return cls(
            tool_name=tool_name,
            status=ToolStatus.SUCCESS,
            result=result,
            call_id=call_id,
            execution_time_ms=execution_time_ms,
            metadata=metadata or {},
        )

    @classmethod
    def error(
        cls,
        tool_name: str,
        error: str,
        status: ToolStatus = ToolStatus.ERROR,
        call_id: str = "",
        execution_time_ms: float = 0.0,
    ) -> "ToolOutput":
        """Factory for error outputs."""
        return cls(
            tool_name=tool_name,
            status=status,
            error=error,
            call_id=call_id,
            execution_time_ms=execution_time_ms,
        )
