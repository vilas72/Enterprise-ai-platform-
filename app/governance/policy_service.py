from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Any

from app.governance.models import (
    PolicyDecision,
    PolicyEffect,
)


@dataclass(slots=True)
class PolicyRule:
    """
    Represents a governance policy rule.

    Wildcards are supported for component, operation and resource.

    Examples:
        component="tool"
        operation="*"
        resource="github:*"

        component="agent"
        operation="execute"

        component="*"
    """

    name: str

    effect: PolicyEffect

    component: str = "*"

    operation: str = "*"

    resource: str = "*"

    priority: int = 100

    enabled: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    required_attributes: dict[str, Any] = field(default_factory=dict)

    description: str | None = None


class PolicyService:
    """
    Enterprise governance policy evaluation engine.

    Responsibilities
    ----------------
    • Register policies
    • Remove policies
    • Evaluate execution requests
    • Apply priority ordering
    • Support wildcard matching
    • Support metadata constraints
    • Produce PolicyDecision

    This service contains no persistence.
    """

    def __init__(self) -> None:

        self._policies: list[PolicyRule] = []

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    async def register_policy(
        self,
        rule: PolicyRule,
    ) -> None:
        """
        Register a policy rule.

        Existing rule with same name will be replaced.
        """

        self._policies = [
            policy
            for policy in self._policies
            if policy.name != rule.name
        ]

        self.validate_policy(rule)
        self._policies.append(rule)

        self._policies.sort(
            key=lambda item: item.priority,
            reverse=True,
        )

    async def register_policies(
        self,
        rules: list[PolicyRule],
    ) -> None:
        """
        Register multiple policies.
        """

        for rule in rules:
            await self.register_policy(rule)

    async def remove_policy(
        self,
        name: str,
    ) -> bool:
        """
        Remove a policy.

        Returns
        -------
        True if removed.
        """

        before = len(self._policies)

        self._policies = [
            policy
            for policy in self._policies
            if policy.name != name
        ]

        return before != len(self._policies)

    async def clear(
        self,
    ) -> None:
        """
        Remove every registered policy.
        """

        self._policies.clear()

    async def list_policies(
        self,
    ) -> list[PolicyRule]:
        """
        Return all policies ordered by priority.
        """

        return list(self._policies)

    async def get_policy(
        self,
        name: str,
    ) -> PolicyRule | None:
        """
        Find policy by name.
        """

        for policy in self._policies:
            if policy.name == name:
                return policy

        return None
    
        # ------------------------------------------------------------------
    # Policy Evaluation
    # ------------------------------------------------------------------

    async def evaluate(
        self,
        *,
        component: str,
        operation: str,
        resource: str = "*",
        metadata: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """
        Evaluate a request against the registered policies.

        Parameters
        ----------
        component:
            Runtime component (tool, agent, ai, connector, ...)

        operation:
            Requested operation.

        resource:
            Target resource.

        metadata:
            Additional context used during evaluation.

        Returns
        -------
        PolicyDecision
        """

        context = metadata or {}

        for policy in self._policies:

            if not policy.enabled:
                continue

            if not self._matches_policy(
                policy=policy,
                component=component,
                operation=operation,
                resource=resource,
                metadata=context,
            ):
                continue

            return PolicyDecision(
                allowed=policy.effect != PolicyEffect.DENY,
                effect=policy.effect,
                reason=policy.description,
                policy_name=policy.name,
                metadata=dict(policy.metadata),
            )

        return PolicyDecision(
            allowed=True,
            effect=PolicyEffect.ALLOW,
            reason="No matching governance policy.",
        )

    async def evaluate_tool(
        self,
        *,
        tool_name: str,
        operation: str = "execute",
        metadata: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """
        Evaluate a tool execution request.
        """

        return await self.evaluate(
            component="tool",
            operation=operation,
            resource=tool_name,
            metadata=metadata,
        )

    async def evaluate_agent(
        self,
        *,
        agent_name: str,
        operation: str,
        metadata: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """
        Evaluate an agent request.
        """

        return await self.evaluate(
            component="agent",
            operation=operation,
            resource=agent_name,
            metadata=metadata,
        )

    async def evaluate_ai_request(
        self,
        *,
        provider: str,
        operation: str,
        metadata: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """
        Evaluate an AI provider request.
        """

        return await self.evaluate(
            component="ai",
            operation=operation,
            resource=provider,
            metadata=metadata,
        )

    async def evaluate_connector(
        self,
        *,
        connector: str,
        operation: str,
        metadata: dict[str, Any] | None = None,
    ) -> PolicyDecision:
        """
        Evaluate an enterprise connector request.
        """

        return await self.evaluate(
            component="connector",
            operation=operation,
            resource=connector,
            metadata=metadata,
        )
        
        # ------------------------------------------------------------------
    # Internal Matching
    # ------------------------------------------------------------------

    def _matches_policy(
        self,
        *,
        policy: PolicyRule,
        component: str,
        operation: str,
        resource: str,
        metadata: dict[str, Any],
    ) -> bool:
        """
        Returns True when the request satisfies every condition of
        the policy rule.
        """

        return (
            self._match_component(policy.component, component)
            and self._match_operation(policy.operation, operation)
            and self._match_resource(policy.resource, resource)
            and self._match_metadata(
                policy.required_attributes,
                metadata,
            )
        )

    @staticmethod
    def _match_component(
        expected: str,
        actual: str,
    ) -> bool:
        """
        Match runtime component.

        Supports shell-style wildcards.

        Examples
        --------
        *
        tool
        agent
        ai
        connector
        """

        return fnmatch(actual.lower(), expected.lower())

    @staticmethod
    def _match_operation(
        expected: str,
        actual: str,
    ) -> bool:
        """
        Match operation name.

        Examples
        --------
        execute
        invoke
        *
        """

        return fnmatch(actual.lower(), expected.lower())

    @staticmethod
    def _match_resource(
        expected: str,
        actual: str,
    ) -> bool:
        """
        Match resource identifier.

        Examples
        --------
        github
        github:repository
        github:*
        *
        """

        return fnmatch(actual.lower(), expected.lower())

    def _match_metadata(
        self,
        required: dict[str, Any],
        actual: dict[str, Any],
    ) -> bool:
        """
        Verify that all required metadata attributes exist and match.

        Supports:

            {"environment": "prod"}

            {"region": "eu*"}

            {"role": "admin"}

        Every required attribute must match.
        """

        if not required:
            return True

        for key, expected in required.items():

            if key not in actual:
                return False

            value = actual[key]

            if not self._match_attribute(
                expected,
                value,
            ):
                return False

        return True

    @staticmethod
    def _match_attribute(
        expected: Any,
        actual: Any,
    ) -> bool:
        """
        Match a single metadata attribute.

        Behaviour
        ---------
        string  -> wildcard matching
        scalar  -> equality
        list    -> membership
        tuple   -> membership
        set     -> membership
        """

        if isinstance(expected, str):
            return fnmatch(
                str(actual).lower(),
                expected.lower(),
            )

        if isinstance(expected, (list, tuple, set)):
            return actual in expected

        return actual == expected
    
        # ------------------------------------------------------------------
    # Policy Management
    # ------------------------------------------------------------------

    async def update_policy(
        self,
        rule: PolicyRule,
    ) -> bool:
        """
        Update an existing policy.

        Returns
        -------
        True if the policy exists and was updated.
        """

        for index, policy in enumerate(self._policies):
            if policy.name == rule.name:
                self._policies[index] = rule
                self._sort_policies()
                return True

        return False

    async def enable_policy(
        self,
        name: str,
    ) -> bool:
        """
        Enable a policy.
        """

        policy = await self.get_policy(name)

        if policy is None:
            return False

        policy.enabled = True
        return True

    async def disable_policy(
        self,
        name: str,
    ) -> bool:
        """
        Disable a policy.
        """

        policy = await self.get_policy(name)

        if policy is None:
            return False

        policy.enabled = False
        return True

    async def has_policy(
        self,
        name: str,
    ) -> bool:
        """
        Returns True if a policy exists.
        """

        return await self.get_policy(name) is not None

    async def count(
        self,
    ) -> int:
        """
        Returns the number of registered policies.
        """

        return len(self._policies)

    async def get_statistics(
        self,
    ) -> dict[str, int]:
        """
        Returns policy statistics.
        """

        enabled = sum(
            1 for policy in self._policies
            if policy.enabled
        )

        disabled = len(self._policies) - enabled

        allow = sum(
            1
            for policy in self._policies
            if policy.effect == PolicyEffect.ALLOW
        )

        deny = sum(
            1
            for policy in self._policies
            if policy.effect == PolicyEffect.DENY
        )

        approval = sum(
            1
            for policy in self._policies
            if policy.effect == PolicyEffect.REQUIRE_APPROVAL
        )

        return {
            "total": len(self._policies),
            "enabled": enabled,
            "disabled": disabled,
            "allow": allow,
            "deny": deny,
            "require_approval": approval,
        }

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_policy(
        self,
        rule: PolicyRule,
    ) -> None:
        """
        Validate a policy definition.

        Raises
        ------
        ValueError
            If the policy is invalid.
        """

        if not rule.name.strip():
            raise ValueError("Policy name cannot be empty.")

        if rule.priority < 0:
            raise ValueError(
                "Policy priority must be greater than or equal to zero."
            )

        if rule.effect not in PolicyEffect:
            raise ValueError(
                "Invalid policy effect."
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _sort_policies(
        self,
    ) -> None:
        """
        Sort policies by priority (highest first).
        """

        self._policies.sort(
            key=lambda policy: policy.priority,
            reverse=True,
        )
        