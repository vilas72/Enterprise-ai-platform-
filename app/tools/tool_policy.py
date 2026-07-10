"""Tool permission and security policy system."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.tools.tool_models import ToolInput, ToolOutput, ToolStatus


class PermissionEffect(str, Enum):
    """Whether a policy rule allows or denies execution."""
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class PolicyRule:
    """
    A single policy rule that allows or denies access to a tool.

    Matching logic (all specified conditions must match):
    - tool_names: if non-empty, only applies to listed tools
    - tags: if non-empty, applies to tools with any of these tags
    - call_id_prefix: if set, only applies to calls whose call_id starts with this

    Empty tool_names + empty tags = applies to ALL tools.
    """

    effect: PermissionEffect
    tool_names: frozenset[str] = field(default_factory=frozenset)
    tags: frozenset[str] = field(default_factory=frozenset)
    call_id_prefix: str = ""
    reason: str = ""


@dataclass
class ToolPolicy:
    """
    Ordered set of PolicyRules evaluated top-to-bottom.

    Default behaviour (when no rules match) is configurable via
    default_effect (default: ALLOW — permissive).

    Evaluation:
    1. Iterate rules in order
    2. First matching rule wins
    3. If no rule matches, apply default_effect

    Usage:
        policy = ToolPolicy(default_effect=PermissionEffect.DENY)
        policy.add_rule(PolicyRule(
            effect=PermissionEffect.ALLOW,
            tags=frozenset(["safe", "math"]),
        ))
    """

    default_effect: PermissionEffect = PermissionEffect.ALLOW
    rules: list[PolicyRule] = field(default_factory=list)

    def add_rule(self, rule: PolicyRule) -> None:
        """Append a rule to the policy."""
        self.rules.append(rule)

    def prepend_rule(self, rule: PolicyRule) -> None:
        """Prepend a rule (highest priority)."""
        self.rules.insert(0, rule)

    def is_allowed(
        self,
        tool_name: str,
        tags: tuple[str, ...],
        call_id: str = "",
    ) -> tuple[bool, str]:
        """
        Check whether a tool call is permitted.

        Args:
            tool_name: Name of the tool being invoked
            tags: Tags from the tool's metadata
            call_id: Optional call identifier

        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        tag_set = set(tags)

        for rule in self.rules:
            if not self._rule_matches(rule, tool_name, tag_set, call_id):
                continue

            allowed = rule.effect == PermissionEffect.ALLOW
            reason = rule.reason or (
                "Allowed by policy." if allowed else "Denied by policy."
            )
            return allowed, reason

        # No rule matched — apply default
        allowed = self.default_effect == PermissionEffect.ALLOW
        reason = (
            "Allowed by default policy."
            if allowed
            else "Denied by default policy (deny-all)."
        )
        return allowed, reason

    @staticmethod
    def _rule_matches(
        rule: PolicyRule,
        tool_name: str,
        tag_set: set[str],
        call_id: str,
    ) -> bool:
        """Return True if all specified conditions in the rule match."""
        if rule.tool_names and tool_name not in rule.tool_names:
            return False
        if rule.tags and not (rule.tags & tag_set):
            return False
        if rule.call_id_prefix and not call_id.startswith(rule.call_id_prefix):
            return False
        return True


class PolicyEnforcingExecutor:
    """
    Wraps ToolExecutor with policy enforcement.

    Checks the ToolPolicy before each execution. Denied calls return a
    PERMISSION_DENIED ToolOutput without ever reaching the tool.

    Usage:
        executor = PolicyEnforcingExecutor(
            tool_executor=ToolExecutor(),
            policy=ToolPolicy(default_effect=PermissionEffect.DENY),
        )
        output = await executor.execute(tool, tool_input)
    """

    def __init__(self, tool_executor, policy: ToolPolicy):
        self._executor = tool_executor
        self._policy = policy

    async def execute(self, tool, tool_input: ToolInput) -> ToolOutput:
        """
        Check policy, then execute if allowed.

        Args:
            tool: Tool to execute
            tool_input: Input payload

        Returns:
            ToolOutput — PERMISSION_DENIED if policy rejects, otherwise
            the result from the underlying executor
        """
        allowed, reason = self._policy.is_allowed(
            tool_name=tool.name,
            tags=tool.metadata.tags,
            call_id=tool_input.call_id,
        )

        if not allowed:
            return ToolOutput.error(
                tool_name=tool.name,
                error=reason,
                status=ToolStatus.PERMISSION_DENIED,
                call_id=tool_input.call_id,
            )

        return await self._executor.execute(tool, tool_input)
