from app.domain.exceptions.provider_exception import ProviderException


class AIProviderException(ProviderException):
    
     def __init__(
        self,
        message: str,
        provider: str,
        status_code: int = 502,
    ):
        super().__init__(
            message=message,
            provider=provider,
        )

        self.status_code = status_code