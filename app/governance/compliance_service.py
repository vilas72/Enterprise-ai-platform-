from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from app.governance.models import ComplianceResult


class ComplianceService:
    """
    Validates requests against enterprise compliance rules.

    This service performs stateless validation and does not own
    persistence. It can be used by AI Runtime, Tool Runtime,
    Agent Runtime and Enterprise Connectors.

    The default implementation validates:

    - Required metadata
    - Required fields
    - Prompt rules
    - AI response rules
    - Tool execution rules
    - Connector rules

    Additional enterprise-specific validators can be registered
    without changing the public interface.
    """

    def __init__(self) -> None:
        self._validators: list = []

    # ------------------------------------------------------------------
    # Validator registration
    # ------------------------------------------------------------------

    async def register_validator(
        self,
        validator,
    ) -> None:
        """
        Register a custom validator.

        Validator signature:

            async def validator(context: dict) -> ComplianceResult
        """

        if validator not in self._validators:
            self._validators.append(validator)

    async def clear_validators(
        self,
    ) -> None:
        """
        Remove all custom validators.
        """

        self._validators.clear()

    # ------------------------------------------------------------------
    # Generic validation
    # ------------------------------------------------------------------

    async def validate(
        self,
        *,
        context: dict[str, Any],
    ) -> ComplianceResult:
        """
        Execute all registered validators.
        """

        violations: list[str] = []
        recommendations: list[str] = []

        for validator in self._validators:

            result: ComplianceResult = await validator(context)

            if not result.compliant:
                violations.extend(result.violations)

            recommendations.extend(result.recommendations)

        return ComplianceResult(
            compliant=len(violations) == 0,
            violations=violations,
            recommendations=recommendations,
        )

    # ------------------------------------------------------------------
    # Prompt validation
    # ------------------------------------------------------------------

    async def validate_prompt(
        self,
        prompt: str,
    ) -> ComplianceResult:
        """
        Validate an LLM prompt.
        """

        violations: list[str] = []

        if not prompt.strip():
            violations.append("Prompt cannot be empty.")

        if len(prompt) > 100_000:
            violations.append(
                "Prompt exceeds maximum supported size."
            )

        return ComplianceResult(
            compliant=not violations,
            violations=violations,
        )

    # ------------------------------------------------------------------
    # Response validation
    # ------------------------------------------------------------------

    async def validate_response(
        self,
        response: str,
    ) -> ComplianceResult:
        """
        Validate an AI response.
        """

        violations: list[str] = []

        if not response.strip():
            violations.append("Response cannot be empty.")

        return ComplianceResult(
            compliant=not violations,
            violations=violations,
        )

    # ------------------------------------------------------------------
    # Tool validation
    # ------------------------------------------------------------------

    async def validate_tool(
        self,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        required_arguments: Iterable[str] | None = None,
    ) -> ComplianceResult:
        """
        Validate a tool execution request.
        """

        violations: list[str] = []

        if not tool_name.strip():
            violations.append("Tool name cannot be empty.")

        if required_arguments:

            for argument in required_arguments:

                if argument not in arguments:
                    violations.append(
                        f"Missing required argument '{argument}'."
                    )

        return ComplianceResult(
            compliant=not violations,
            violations=violations,
        )

    # ------------------------------------------------------------------
    # Connector validation
    # ------------------------------------------------------------------

    async def validate_connector(
        self,
        *,
        connector_name: str,
        operation: str,
    ) -> ComplianceResult:
        """
        Validate an enterprise connector request.
        """

        violations: list[str] = []

        if not connector_name.strip():
            violations.append(
                "Connector name cannot be empty."
            )

        if not operation.strip():
            violations.append(
                "Connector operation cannot be empty."
            )

        return ComplianceResult(
            compliant=not violations,
            violations=violations,
        )

    # ------------------------------------------------------------------
    # Metadata validation
    # ------------------------------------------------------------------

    async def validate_required_fields(
        self,
        *,
        data: dict[str, Any],
        required_fields: Iterable[str],
    ) -> ComplianceResult:
        """
        Validate required fields.
        """

        violations: list[str] = []

        for field in required_fields:

            value = data.get(field)

            if value is None:
                violations.append(
                    f"Required field '{field}' is missing."
                )
                continue

            if isinstance(value, str) and not value.strip():
                violations.append(
                    f"Required field '{field}' is empty."
                )

        return ComplianceResult(
            compliant=not violations,
            violations=violations,
        )