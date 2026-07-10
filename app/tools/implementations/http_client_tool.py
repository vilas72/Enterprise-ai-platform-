"""HTTPClient tool — makes HTTP GET/POST requests to allowed domains."""

from __future__ import annotations

import json
from urllib.parse import urlparse

from app.tools.base_tool import Tool
from app.tools.tool_models import (
    ToolInput,
    ToolMetadata,
    ToolOutput,
    ToolParameter,
    ToolStatus,
)

_DEFAULT_TIMEOUT_SECONDS = 10
_MAX_RESPONSE_BYTES = 500 * 1024  # 500 KB


class HTTPClientTool(Tool):
    """
    Makes HTTP GET and POST requests to whitelisted domains.

    Security:
    - Only allows HTTPS (configurable)
    - Domain allowlist prevents SSRF attacks
    - Response size cap prevents memory exhaustion

    Example:
        Input: {"url": "https://api.example.com/data", "method": "GET"}
        Output: {"status_code": 200, "body": "...", "headers": {...}}
    """

    _METADATA = ToolMetadata(
        name="http_client",
        description=(
            "Makes HTTP GET or POST requests to external APIs. "
            "Only whitelisted domains are accessible."
        ),
        parameters=(
            ToolParameter(
                name="url",
                type="string",
                description="Full URL to request (must be HTTPS).",
                required=True,
            ),
            ToolParameter(
                name="method",
                type="string",
                description="HTTP method: 'GET' or 'POST'.",
                required=False,
                default="GET",
            ),
            ToolParameter(
                name="body",
                type="object",
                description="Request body for POST requests (will be JSON-encoded).",
                required=False,
                default=None,
            ),
            ToolParameter(
                name="headers",
                type="object",
                description="Additional HTTP headers as key-value pairs.",
                required=False,
                default=None,
            ),
        ),
        tags=("network", "http"),
        version="1.0.0",
    )

    def __init__(
        self,
        allowed_domains: list[str],
        require_https: bool = True,
        timeout_seconds: int = _DEFAULT_TIMEOUT_SECONDS,
    ):
        """
        Args:
            allowed_domains: Whitelisted domain names (e.g. ["api.example.com"])
            require_https: Reject non-HTTPS URLs (recommended: True)
            timeout_seconds: Per-request timeout
        """
        self._allowed_domains = set(allowed_domains)
        self._require_https = require_https
        self._timeout = timeout_seconds

    @property
    def metadata(self) -> ToolMetadata:
        return self._METADATA

    async def execute(self, tool_input: ToolInput) -> ToolOutput:
        url = tool_input.require("url")
        method = (tool_input.get("method", "GET") or "GET").upper()
        body = tool_input.get("body")
        extra_headers: dict = tool_input.get("headers") or {}

        # Validate method
        if method not in {"GET", "POST"}:
            return ToolOutput.error(
                tool_name=self.name,
                error=f"Unsupported HTTP method: '{method}'. Use GET or POST.",
                call_id=tool_input.call_id,
            )

        # Validate URL
        url_error = self._validate_url(url)
        if url_error:
            return ToolOutput.error(
                tool_name=self.name,
                error=url_error,
                status=ToolStatus.PERMISSION_DENIED,
                call_id=tool_input.call_id,
            )

        try:
            import aiohttp
        except ImportError:
            return ToolOutput.error(
                tool_name=self.name,
                error=(
                    "aiohttp is required for HTTPClientTool. "
                    "Install it with: pip install aiohttp"
                ),
                call_id=tool_input.call_id,
            )

        try:
            return await self._make_request(
                url=url,
                method=method,
                body=body,
                headers=extra_headers,
                tool_input=tool_input,
            )
        except Exception as exc:
            return ToolOutput.error(
                tool_name=self.name,
                error=f"Request failed: {type(exc).__name__}: {exc}",
                call_id=tool_input.call_id,
            )

    async def _make_request(
        self,
        url: str,
        method: str,
        body,
        headers: dict,
        tool_input: ToolInput,
    ) -> ToolOutput:
        import aiohttp

        request_headers = {"Content-Type": "application/json", **headers}
        timeout = aiohttp.ClientTimeout(total=self._timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            request_kwargs = {"headers": request_headers}
            if method == "POST" and body is not None:
                request_kwargs["json"] = body

            async with session.request(method, url, **request_kwargs) as response:
                raw = await response.content.read(_MAX_RESPONSE_BYTES)
                body_text = raw.decode("utf-8", errors="replace")

                return ToolOutput.success(
                    tool_name=self.name,
                    result={
                        "status_code": response.status,
                        "body": body_text,
                        "headers": dict(response.headers),
                        "url": str(response.url),
                    },
                    call_id=tool_input.call_id,
                )

    def _validate_url(self, url: str) -> str | None:
        """Return error message if URL is not allowed, else None."""
        try:
            parsed = urlparse(url)
        except Exception:
            return f"Invalid URL: '{url}'"

        if self._require_https and parsed.scheme != "https":
            return (
                f"Only HTTPS URLs are allowed. Got scheme: '{parsed.scheme}'."
            )

        domain = parsed.netloc.split(":")[0]  # strip port
        if self._allowed_domains and domain not in self._allowed_domains:
            return (
                f"Domain '{domain}' is not in the allowlist. "
                f"Allowed: {sorted(self._allowed_domains)}"
            )

        return None
