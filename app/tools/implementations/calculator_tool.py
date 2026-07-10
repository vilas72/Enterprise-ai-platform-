"""Calculator tool — safe arithmetic evaluation."""

from __future__ import annotations

import ast
import operator
from typing import Any

from app.tools.base_tool import Tool
from app.tools.tool_models import (
    ToolInput,
    ToolMetadata,
    ToolOutput,
    ToolParameter,
)

# Safe subset of arithmetic operators
_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_MAX_EXPRESSION_LENGTH = 500


class CalculatorTool(Tool):
    """
    Evaluates arithmetic expressions safely.

    Supports: + - * / ** % // and nested parentheses.
    Does NOT support: function calls, variable access, imports, or any
    non-numeric operations. This prevents code injection.

    Example:
        Input: {"expression": "2 ** 10 + 100 / 4"}
        Output: {"result": 1049.0, "expression": "2 ** 10 + 100 / 4"}
    """

    _METADATA = ToolMetadata(
        name="calculator",
        description=(
            "Evaluates arithmetic expressions. "
            "Supports +, -, *, /, **, %, //. "
            "Example: '(3 + 5) * 2' returns 16."
        ),
        parameters=(
            ToolParameter(
                name="expression",
                type="string",
                description="Arithmetic expression to evaluate (e.g. '2 + 2')",
                required=True,
            ),
        ),
        tags=("math", "safe"),
        version="1.0.0",
    )

    @property
    def metadata(self) -> ToolMetadata:
        return self._METADATA

    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        expression = tool_input.require("expression")

        if not isinstance(expression, str):
            return ToolOutput.error(
                tool_name=self.name,
                error="'expression' must be a string.",
                call_id=tool_input.call_id,
            )

        if len(expression) > _MAX_EXPRESSION_LENGTH:
            return ToolOutput.error(
                tool_name=self.name,
                error=(
                    f"Expression too long (max {_MAX_EXPRESSION_LENGTH} chars)."
                ),
                call_id=tool_input.call_id,
            )

        try:
            result = self._safe_eval(expression)
            return ToolOutput.success(
                tool_name=self.name,
                result={"result": result, "expression": expression},
                call_id=tool_input.call_id,
            )
        except ZeroDivisionError:
            return ToolOutput.error(
                tool_name=self.name,
                error="Division by zero.",
                call_id=tool_input.call_id,
            )
        except Exception as exc:
            return ToolOutput.error(
                tool_name=self.name,
                error=f"Could not evaluate expression: {exc}",
                call_id=tool_input.call_id,
            )

    def _safe_eval(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression using AST parsing.

        Only numeric literals and safe arithmetic operations are allowed.
        Any other node type raises ValueError.
        """
        tree = ast.parse(expression, mode="eval")
        return self._eval_node(tree.body)

    def _eval_node(self, node: ast.expr) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in _SAFE_OPS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return _SAFE_OPS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in _SAFE_OPS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            operand = self._eval_node(node.operand)
            return _SAFE_OPS[op_type](operand)

        raise ValueError(f"Unsupported expression node: {type(node).__name__}")
