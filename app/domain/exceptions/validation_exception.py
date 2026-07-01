from app.domain.exceptions.base_exception import EnterpriseException


class ValidationException(EnterpriseException):
    def __init__(
        self,
        message: str,
        field: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={
                "field": field
            },
        )