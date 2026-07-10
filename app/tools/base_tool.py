"""Abstract base class for all tools."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.tools.tool_models import ToolInput, ToolMetadata, ToolOutput


class Tool(ABC):
    """
    Abstract base class that all tools must implement.

    A tool is a discrete, invocable capability that an AI agent can use.
    Each tool declares its interface via ToolMetadata and implements a
    single async execute() method.

    Convention:
    - Tools are stateless between calls (all state lives in ToolInput)
    - execute() must never raise — wrap exceptions in ToolOutput.error()
    - Metadata.name must match the class registration key
    """

    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Return static metadata describing this tool's interface."""
        ...

    @abstractmethod
    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        """
        Execute the tool with the given input.

        Must not raise exceptions. All errors should be returned as
        ToolOutput.error(...) with an appropriate ToolStatus.

        Args:
            tool_input: Validated input payload

        Returns:
            ToolOutput containing the result or error information
        """
        ...

    @property
    def name(self) -> str:
        """Shortcut for metadata.name."""
        return self.metadata.name
