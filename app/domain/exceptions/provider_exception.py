from app.domain.exceptions.base_exception import EnterpriseException


class ProviderException(EnterpriseException):
    def __init__(
        self,
        message: str,
        provider: str,
    ) -> None:
        super().__init__(
            message=message,
            error_code="PROVIDER_ERROR",
            details={
                "provider": provider
            },
        )