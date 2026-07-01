from __future__ import annotations

from typing import Any


class EnterpriseException(Exception):

    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        details: dict | None = None,
    ):
        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.details = details or {}