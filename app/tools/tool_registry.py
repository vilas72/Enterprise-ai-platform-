"""Tool registry — central store for discovering and managing tools."""

from __future__ import annotations

from app.tools.base_tool import Tool
from app.tools.tool_models import ToolMetadata


class ToolNotFoundError(Exception):
    """Raised when a requested tool is not registered."""
    pass


class ToolAlreadyRegisteredError(Exception):
    """Raised when a tool name is already taken."""
    pass


class ToolRegistry:
    """
    Central registry for all available tools.

    Supports:
    - Registration / unregistration by tool name
    - Retrieval by name
    - Discovery: list all tools, filter by tag
    - Schema generation for LLM prompt injection

    Usage:
        registry = ToolRegistry()
        registry.register(CalculatorTool())
        registry.register(FileReaderTool())

        tool = registry.get("calculator")
        math_tools = registry.find_by_tag("math")
        schema = registry.to_schema()  # For LLM system prompts
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------

    def register(self, tool: Tool, *, overwrite: bool = False) -> None:
        """
        Register a tool instance.

        Args:
            tool: Tool instance to register
            overwrite: If True, silently replace existing registration

        Raises:
            ToolAlreadyRegisteredError: If tool name is taken and overwrite=False
        """
        name = tool.name
        if name in self._tools and not overwrite:
            raise ToolAlreadyRegisteredError(
                f"Tool '{name}' is already registered. "
                "Pass overwrite=True to replace it."
            )
        self._tools[name] = tool

    def unregister(self, tool_name: str) -> None:
        """
        Remove a tool from the registry.

        Raises:
            ToolNotFoundError: If the tool name is not registered
        """
        if tool_name not in self._tools:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' is not registered."
            )
        del self._tools[tool_name]

    # -------------------------------------------------------------------------
    # Retrieval
    # -------------------------------------------------------------------------

    def get(self, tool_name: str) -> Tool:
        """
        Retrieve a registered tool by name.

        Raises:
            ToolNotFoundError: If the tool is not registered
        """
        if tool_name not in self._tools:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' is not registered. "
                f"Available: {self.list_tools()}"
            )
        return self._tools[tool_name]

    def is_registered(self, tool_name: str) -> bool:
        """Return True if the tool name is registered."""
        return tool_name in self._tools

    # -------------------------------------------------------------------------
    # Discovery
    # -------------------------------------------------------------------------

    def list_tools(self) -> list[str]:
        """Return a sorted list of all registered tool names."""
        return sorted(self._tools.keys())

    def find_by_tag(self, tag: str) -> list[Tool]:
        """
        Return all tools that have the given tag.

        Args:
            tag: Tag string to filter by (e.g. "math", "safe", "network")

        Returns:
            List of matching Tool instances (may be empty)
        """
        return [
            tool
            for tool in self._tools.values()
            if tag in tool.metadata.tags
        ]

    def all_metadata(self) -> list[ToolMetadata]:
        """Return metadata for all registered tools, sorted by name."""
        return [
            self._tools[name].metadata
            for name in sorted(self._tools)
        ]

    # -------------------------------------------------------------------------
    # Schema generation for LLM prompts
    # -------------------------------------------------------------------------

    def to_schema(self) -> list[dict]:
        """
        Generate an OpenAI-compatible tool schema for all registered tools.

        Returns:
            List of tool definition dicts suitable for use in chat completions
            or system prompt injection.
        """
        schemas = []
        for tool in self._tools.values():
            meta = tool.metadata
            properties = {}
            required_params = []

            for param in meta.parameters:
                properties[param.name] = {
                    "type": param.type,
                    "description": param.description,
                }
                if param.default is not None:
                    properties[param.name]["default"] = param.default
                if param.required:
                    required_params.append(param.name)

            schemas.append({
                "type": "function",
                "function": {
                    "name": meta.name,
                    "description": meta.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required_params,
                    },
                },
            })

        return schemas

    # -------------------------------------------------------------------------
    # Dunder
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._tools)

    def __repr__(self) -> str:
        return f"ToolRegistry(tools={self.list_tools()})"
