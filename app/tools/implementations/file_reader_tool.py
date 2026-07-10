"""FileReader tool — reads text files from allowed paths."""

from __future__ import annotations

import os
from pathlib import Path

from app.tools.base_tool import Tool
from app.tools.tool_models import (
    ToolInput,
    ToolMetadata,
    ToolOutput,
    ToolParameter,
    ToolStatus,
)

_MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB


class FileReaderTool(Tool):
    """
    Reads the text content of a file within an allowed root directory.

    Security:
    - Restricts access to files within the configured allowed_root
    - Blocks path traversal attempts (../../etc/passwd)
    - Enforces a file size limit to prevent memory exhaustion

    Example:
        Input: {"path": "/data/knowledge/overview.txt"}
        Output: {"content": "...", "path": "...", "size_bytes": 1024}
    """

    _METADATA = ToolMetadata(
        name="file_reader",
        description=(
            "Reads the text content of a file. "
            "Only files within the permitted directory are accessible."
        ),
        parameters=(
            ToolParameter(
                name="path",
                type="string",
                description="Absolute path to the file to read.",
                required=True,
            ),
            ToolParameter(
                name="encoding",
                type="string",
                description="File encoding (default: utf-8).",
                required=False,
                default="utf-8",
            ),
        ),
        tags=("filesystem", "read-only"),
        version="1.0.0",
    )

    def __init__(self, allowed_root: str):
        """
        Args:
            allowed_root: Base directory. All read requests must resolve
                          to a path inside this directory.
        """
        self._allowed_root = Path(allowed_root).resolve()

    @property
    def metadata(self) -> ToolMetadata:
        return self._METADATA

    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        raw_path = tool_input.require("path")
        encoding = tool_input.get("encoding", "utf-8")

        try:
            file_path = Path(raw_path).resolve()
        except Exception:
            return ToolOutput.error(
                tool_name=self.name,
                error=f"Invalid path: {raw_path}",
                call_id=tool_input.call_id,
            )

        # Security: enforce allowed root boundary
        try:
            file_path.relative_to(self._allowed_root)
        except ValueError:
            return ToolOutput.error(
                tool_name=self.name,
                error=(
                    f"Access denied: '{file_path}' is outside the "
                    f"permitted directory '{self._allowed_root}'."
                ),
                status=ToolStatus.PERMISSION_DENIED,
                call_id=tool_input.call_id,
            )

        if not file_path.exists():
            return ToolOutput.error(
                tool_name=self.name,
                error=f"File not found: '{file_path}'",
                status=ToolStatus.NOT_FOUND,
                call_id=tool_input.call_id,
            )

        if not file_path.is_file():
            return ToolOutput.error(
                tool_name=self.name,
                error=f"Path is not a file: '{file_path}'",
                call_id=tool_input.call_id,
            )

        size = file_path.stat().st_size
        if size > _MAX_FILE_SIZE_BYTES:
            return ToolOutput.error(
                tool_name=self.name,
                error=(
                    f"File too large ({size} bytes). "
                    f"Maximum allowed: {_MAX_FILE_SIZE_BYTES} bytes."
                ),
                call_id=tool_input.call_id,
            )

        try:
            content = file_path.read_text(encoding=encoding)
            return ToolOutput.success(
                tool_name=self.name,
                result={
                    "content": content,
                    "path": str(file_path),
                    "size_bytes": size,
                    "encoding": encoding,
                },
                call_id=tool_input.call_id,
            )
        except UnicodeDecodeError:
            return ToolOutput.error(
                tool_name=self.name,
                error=(
                    f"Could not decode file with encoding '{encoding}'. "
                    "Try encoding='latin-1'."
                ),
                call_id=tool_input.call_id,
            )
        except Exception as exc:
            return ToolOutput.error(
                tool_name=self.name,
                error=f"Failed to read file: {exc}",
                call_id=tool_input.call_id,
            )
