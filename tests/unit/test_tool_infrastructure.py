"""Tests for Phase 3 — Tool infrastructure (models, executor, registry, policy, implementations)."""

import asyncio
import pytest
from pathlib import Path
from unittest.mock import AsyncMock

from app.tools.tool_models import (
    ToolInput,
    ToolMetadata,
    ToolOutput,
    ToolParameter,
    ToolStatus,
)
from app.tools.base_tool import Tool
from app.tools.tool_executor import ToolExecutor
from app.tools.tool_registry import ToolRegistry, ToolNotFoundError, ToolAlreadyRegisteredError
from app.tools.tool_policy import (
    ToolPolicy,
    PolicyRule,
    PermissionEffect,
    PolicyEnforcingExecutor,
)
from app.tools.implementations.calculator_tool import CalculatorTool
from app.tools.implementations.file_reader_tool import FileReaderTool


# ---------------------------------------------------------------------------
# Test double tool
# ---------------------------------------------------------------------------

class EchoTool(Tool):
    """Returns its input as output. Used for testing the framework."""

    _META = ToolMetadata(
        name="echo",
        description="Echoes the input message.",
        parameters=(
            ToolParameter(name="message", type="string", description="Message", required=True),
            ToolParameter(name="prefix", type="string", description="Prefix", required=False, default=""),
        ),
        tags=("safe", "test"),
        version="1.0.0",
    )

    @property
    def metadata(self) -> ToolMetadata:
        return self._META

    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        message = tool_input.require("message")
        prefix = tool_input.get("prefix", "")
        return ToolOutput.success(
            tool_name=self.name,
            result=f"{prefix}{message}",
            call_id=tool_input.call_id,
        )


class AlwaysErrorTool(Tool):
    _META = ToolMetadata(
        name="always_error",
        description="Always raises an exception.",
        parameters=(),
        tags=("test",),
    )

    @property
    def metadata(self) -> ToolMetadata:
        return self._META

    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        raise RuntimeError("This tool always fails.")


class SlowTool(Tool):
    _META = ToolMetadata(
        name="slow_tool",
        description="Sleeps forever.",
        parameters=(),
        tags=("test",),
    )

    @property
    def metadata(self) -> ToolMetadata:
        return self._META

    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        await asyncio.sleep(9999)
        return ToolOutput.success(tool_name=self.name, result="done")


# ===========================================================================
# ToolModels tests
# ===========================================================================

class TestToolInput:

    def test_get_returns_value(self):
        ti = ToolInput(tool_name="t", parameters={"x": 42})
        assert ti.get("x") == 42

    def test_get_returns_default(self):
        ti = ToolInput(tool_name="t", parameters={})
        assert ti.get("missing", "default") == "default"

    def test_require_returns_value(self):
        ti = ToolInput(tool_name="t", parameters={"key": "val"})
        assert ti.require("key") == "val"

    def test_require_raises_on_missing(self):
        ti = ToolInput(tool_name="t", parameters={})
        with pytest.raises(KeyError, match="Required parameter"):
            ti.require("missing")


class TestToolOutput:

    def test_success_factory(self):
        out = ToolOutput.success(tool_name="t", result=42, call_id="abc")
        assert out.is_success
        assert not out.is_error
        assert out.result == 42
        assert out.call_id == "abc"

    def test_error_factory(self):
        out = ToolOutput.error(tool_name="t", error="oops", call_id="xyz")
        assert out.is_error
        assert out.error == "oops"
        assert out.status == ToolStatus.ERROR

    def test_timeout_status(self):
        out = ToolOutput.error(
            tool_name="t",
            error="timed out",
            status=ToolStatus.TIMEOUT,
        )
        assert out.status == ToolStatus.TIMEOUT
        assert out.is_error


# ===========================================================================
# ToolExecutor tests
# ===========================================================================

@pytest.mark.asyncio
class TestToolExecutor:

    async def test_execute_success(self):
        executor = ToolExecutor()
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={"message": "hello"})
        output = await executor.execute(tool, ti)
        assert output.is_success
        assert output.result == "hello"

    async def test_execute_with_optional_param(self):
        executor = ToolExecutor()
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={"message": "hi", "prefix": ">> "})
        output = await executor.execute(tool, ti)
        assert output.result == ">> hi"

    async def test_execute_missing_required_returns_error(self):
        executor = ToolExecutor()
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={})  # Missing 'message'
        output = await executor.execute(tool, ti)
        assert output.is_error
        assert "message" in output.error

    async def test_execute_isolates_exceptions(self):
        executor = ToolExecutor()
        tool = AlwaysErrorTool()
        ti = ToolInput(tool_name="always_error", parameters={})
        output = await executor.execute(tool, ti)
        assert output.is_error
        assert "RuntimeError" in output.error

    async def test_execute_timeout(self):
        executor = ToolExecutor(timeout_seconds=0.05)
        tool = SlowTool()
        ti = ToolInput(tool_name="slow_tool", parameters={})
        output = await executor.execute(tool, ti)
        assert output.status == ToolStatus.TIMEOUT

    async def test_execute_sets_execution_time(self):
        executor = ToolExecutor()
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={"message": "x"})
        output = await executor.execute(tool, ti)
        assert output.execution_time_ms > 0

    async def test_execute_preserves_call_id(self):
        executor = ToolExecutor()
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={"message": "x"}, call_id="req-99")
        output = await executor.execute(tool, ti)
        assert output.call_id == "req-99"


# ===========================================================================
# ToolRegistry tests
# ===========================================================================

class TestToolRegistry:

    def test_register_and_get(self):
        registry = ToolRegistry()
        tool = EchoTool()
        registry.register(tool)
        assert registry.get("echo") is tool

    def test_register_duplicate_raises(self):
        registry = ToolRegistry()
        registry.register(EchoTool())
        with pytest.raises(ToolAlreadyRegisteredError):
            registry.register(EchoTool())

    def test_register_with_overwrite(self):
        registry = ToolRegistry()
        t1 = EchoTool()
        t2 = EchoTool()
        registry.register(t1)
        registry.register(t2, overwrite=True)
        assert registry.get("echo") is t2

    def test_unregister(self):
        registry = ToolRegistry()
        registry.register(EchoTool())
        registry.unregister("echo")
        assert not registry.is_registered("echo")

    def test_unregister_nonexistent_raises(self):
        registry = ToolRegistry()
        with pytest.raises(ToolNotFoundError):
            registry.unregister("ghost")

    def test_get_nonexistent_raises(self):
        registry = ToolRegistry()
        with pytest.raises(ToolNotFoundError, match="not registered"):
            registry.get("unknown")

    def test_list_tools_sorted(self):
        registry = ToolRegistry()
        registry.register(EchoTool())
        registry.register(AlwaysErrorTool())
        assert registry.list_tools() == ["always_error", "echo"]

    def test_find_by_tag(self):
        registry = ToolRegistry()
        registry.register(EchoTool())      # tags: safe, test
        registry.register(AlwaysErrorTool())  # tags: test
        safe_tools = registry.find_by_tag("safe")
        assert len(safe_tools) == 1
        assert safe_tools[0].name == "echo"

    def test_find_by_tag_empty(self):
        registry = ToolRegistry()
        registry.register(EchoTool())
        assert registry.find_by_tag("nonexistent") == []

    def test_to_schema_structure(self):
        registry = ToolRegistry()
        registry.register(EchoTool())
        schema = registry.to_schema()
        assert len(schema) == 1
        assert schema[0]["type"] == "function"
        fn = schema[0]["function"]
        assert fn["name"] == "echo"
        assert "message" in fn["parameters"]["properties"]
        assert "message" in fn["parameters"]["required"]

    def test_len(self):
        registry = ToolRegistry()
        assert len(registry) == 0
        registry.register(EchoTool())
        assert len(registry) == 1

    def test_all_metadata(self):
        registry = ToolRegistry()
        registry.register(EchoTool())
        metas = registry.all_metadata()
        assert len(metas) == 1
        assert metas[0].name == "echo"


# ===========================================================================
# ToolPolicy tests
# ===========================================================================

class TestToolPolicy:

    def test_default_allow(self):
        policy = ToolPolicy(default_effect=PermissionEffect.ALLOW)
        allowed, _ = policy.is_allowed("any_tool", ())
        assert allowed

    def test_default_deny(self):
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        allowed, _ = policy.is_allowed("any_tool", ())
        assert not allowed

    def test_allow_rule_by_tag(self):
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.ALLOW,
            tags=frozenset(["safe"]),
        ))
        allowed, _ = policy.is_allowed("echo", ("safe", "test"))
        assert allowed

    def test_deny_rule_by_tool_name(self):
        policy = ToolPolicy(default_effect=PermissionEffect.ALLOW)
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.DENY,
            tool_names=frozenset(["dangerous_tool"]),
            reason="Dangerous tool blocked.",
        ))
        allowed, reason = policy.is_allowed("dangerous_tool", ())
        assert not allowed
        assert "Dangerous" in reason

    def test_first_matching_rule_wins(self):
        policy = ToolPolicy(default_effect=PermissionEffect.ALLOW)
        # Rule 1: deny tool named "echo"
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.DENY,
            tool_names=frozenset(["echo"]),
        ))
        # Rule 2: allow tag "safe"
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.ALLOW,
            tags=frozenset(["safe"]),
        ))
        # Rule 1 should win because it's first and matches
        allowed, _ = policy.is_allowed("echo", ("safe", "test"))
        assert not allowed

    def test_no_matching_rule_uses_default(self):
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.ALLOW,
            tool_names=frozenset(["specific_tool"]),
        ))
        allowed, _ = policy.is_allowed("other_tool", ())
        assert not allowed  # Default deny

    def test_prepend_rule_has_priority(self):
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.ALLOW,
            tags=frozenset(["safe"]),
        ))
        policy.prepend_rule(PolicyRule(
            effect=PermissionEffect.DENY,
            tags=frozenset(["safe"]),
            reason="Overridden.",
        ))
        allowed, _ = policy.is_allowed("echo", ("safe",))
        assert not allowed


@pytest.mark.asyncio
class TestPolicyEnforcingExecutor:

    async def test_allows_permitted_tool(self):
        policy = ToolPolicy(default_effect=PermissionEffect.ALLOW)
        executor = PolicyEnforcingExecutor(ToolExecutor(), policy)
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={"message": "ok"})
        output = await executor.execute(tool, ti)
        assert output.is_success

    async def test_blocks_denied_tool(self):
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        executor = PolicyEnforcingExecutor(ToolExecutor(), policy)
        tool = EchoTool()
        ti = ToolInput(tool_name="echo", parameters={"message": "blocked"})
        output = await executor.execute(tool, ti)
        assert output.status == ToolStatus.PERMISSION_DENIED

    async def test_permission_denied_does_not_call_tool(self):
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        executor = PolicyEnforcingExecutor(ToolExecutor(), policy)
        tool = AlwaysErrorTool()
        ti = ToolInput(tool_name="always_error", parameters={})
        output = await executor.execute(tool, ti)
        # Should be PERMISSION_DENIED, not ERROR from the tool's exception
        assert output.status == ToolStatus.PERMISSION_DENIED


# ===========================================================================
# CalculatorTool tests
# ===========================================================================

@pytest.mark.asyncio
class TestCalculatorTool:

    async def test_addition(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "2 + 3"})
        out = await tool.execute(ti)
        assert out.is_success
        assert out.result["result"] == 5.0

    async def test_subtraction(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "10 - 4"})
        out = await tool.execute(ti)
        assert out.result["result"] == 6.0

    async def test_multiplication(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "3 * 7"})
        out = await tool.execute(ti)
        assert out.result["result"] == 21.0

    async def test_division(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "10 / 4"})
        out = await tool.execute(ti)
        assert out.result["result"] == 2.5

    async def test_power(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "2 ** 10"})
        out = await tool.execute(ti)
        assert out.result["result"] == 1024.0

    async def test_complex_expression(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "(3 + 5) * 2 - 1"})
        out = await tool.execute(ti)
        assert out.result["result"] == 15.0

    async def test_negative_number(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "-5 + 3"})
        out = await tool.execute(ti)
        assert out.result["result"] == -2.0

    async def test_division_by_zero(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "1 / 0"})
        out = await tool.execute(ti)
        assert out.is_error
        assert "zero" in out.error.lower()

    async def test_invalid_expression(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "import os"})
        out = await tool.execute(ti)
        assert out.is_error

    async def test_function_call_blocked(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "abs(-5)"})
        out = await tool.execute(ti)
        assert out.is_error

    async def test_result_includes_expression(self):
        tool = CalculatorTool()
        ti = ToolInput(tool_name="calculator", parameters={"expression": "1 + 1"})
        out = await tool.execute(ti)
        assert out.result["expression"] == "1 + 1"

    def test_calculator_metadata(self):
        tool = CalculatorTool()
        assert tool.name == "calculator"
        assert "math" in tool.metadata.tags


# ===========================================================================
# FileReaderTool tests
# ===========================================================================

@pytest.mark.asyncio
class TestFileReaderTool:

    async def test_read_file_in_allowed_root(self, tmp_path: Path):
        (tmp_path / "notes.txt").write_text("Hello from notes.")
        tool = FileReaderTool(allowed_root=str(tmp_path))
        ti = ToolInput(
            tool_name="file_reader",
            parameters={"path": str(tmp_path / "notes.txt")},
        )
        out = await tool.execute(ti)
        assert out.is_success
        assert out.result["content"] == "Hello from notes."
        assert out.result["size_bytes"] > 0

    async def test_blocks_path_traversal(self, tmp_path: Path):
        allowed = tmp_path / "allowed"
        allowed.mkdir()
        (tmp_path / "secret.txt").write_text("secret")

        tool = FileReaderTool(allowed_root=str(allowed))
        ti = ToolInput(
            tool_name="file_reader",
            parameters={"path": str(tmp_path / "secret.txt")},
        )
        out = await tool.execute(ti)
        assert out.status == ToolStatus.PERMISSION_DENIED

    async def test_file_not_found(self, tmp_path: Path):
        tool = FileReaderTool(allowed_root=str(tmp_path))
        ti = ToolInput(
            tool_name="file_reader",
            parameters={"path": str(tmp_path / "missing.txt")},
        )
        out = await tool.execute(ti)
        assert out.status == ToolStatus.NOT_FOUND

    async def test_large_file_blocked(self, tmp_path: Path):
        big = tmp_path / "big.txt"
        big.write_bytes(b"x" * (2 * 1024 * 1024))  # 2 MB
        tool = FileReaderTool(allowed_root=str(tmp_path))
        ti = ToolInput(
            tool_name="file_reader",
            parameters={"path": str(big)},
        )
        out = await tool.execute(ti)
        assert out.is_error
        assert "too large" in out.error.lower()

    async def test_file_reader_metadata(self, tmp_path: Path):
        tool = FileReaderTool(allowed_root=str(tmp_path))
        assert tool.name == "file_reader"
        assert "filesystem" in tool.metadata.tags
