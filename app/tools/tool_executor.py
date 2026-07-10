"""Tool executor — lifecycle management for tool invocations."""

from __future__ import annotations

import asyncio
import time

from app.tools.base_tool import Tool
from app.tools.tool_models import ToolInput, ToolOutput, ToolStatus


class ToolExecutor:
    """
    Manages the execution lifecycle for tool calls.

    Responsibilities:
    - Input validation against tool metadata
    - Async execution with configurable timeout
    - Execution timing measurement
    - Exception isolation (errors never propagate to callers)

    Usage:
        executor = ToolExecutor(timeout_seconds=10.0)
        output = await executor.execute(tool, tool_input)
    """

    def __init__(self, timeout_seconds: float = 30.0):
        """
        Args:
            timeout_seconds: Maximum allowed execution time per tool call.
                             Calls exceeding this are cancelled and return
                             a TIMEOUT status.
        """
        self._timeout = timeout_seconds

    async def execute(
        self,
        tool: Tool,
        tool_input: ToolInput,
    ) -> ToolOutput:
        """
        Execute a tool with timeout and error isolation.

        Args:
            tool: The tool to execute
            tool_input: Input payload

        Returns:
            ToolOutput — never raises
        """
        # Validate required parameters before executing
        validation_error = self._validate_input(tool, tool_input)
        if validation_error:
            return ToolOutput.error(
                tool_name=tool.name,
                error=validation_error,
                status=ToolStatus.ERROR,
                call_id=tool_input.call_id,
            )

        start_time = time.perf_counter()

        try:
            output = await asyncio.wait_for(
                tool.execute(tool_input),
                timeout=self._timeout,
            )
            # Inject timing if not already set
            if output.execution_time_ms == 0.0:
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                output = ToolOutput(
                    tool_name=output.tool_name,
                    status=output.status,
                    result=output.result,
                    error=output.error,
                    call_id=output.call_id,
                    execution_time_ms=elapsed_ms,
                    metadata=output.metadata,
                )
            return output

        except asyncio.TimeoutError:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ToolOutput.error(
                tool_name=tool.name,
                error=(
                    f"Tool '{tool.name}' timed out after "
                    f"{self._timeout:.1f}s."
                ),
                status=ToolStatus.TIMEOUT,
                call_id=tool_input.call_id,
                execution_time_ms=elapsed_ms,
            )

        except Exception as exc:  # noqa: BLE001
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return ToolOutput.error(
                tool_name=tool.name,
                error=f"{type(exc).__name__}: {exc}",
                status=ToolStatus.ERROR,
                call_id=tool_input.call_id,
                execution_time_ms=elapsed_ms,
            )

    @staticmethod
    def _validate_input(tool: Tool, tool_input: ToolInput) -> str | None:
        """
        Validate that all required parameters are present.

        Returns:
            Error message string if invalid, None if valid
        """
        missing = [
            param.name
            for param in tool.metadata.parameters
            if param.required and param.name not in tool_input.parameters
        ]
        if missing:
            return (
                f"Missing required parameters for '{tool.name}': "
                f"{missing}"
            )
        return None
