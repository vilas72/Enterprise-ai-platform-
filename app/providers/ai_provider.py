from abc import ABC, abstractmethod
from collections.abc import Generator

from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse


class AIProvider(ABC):

    @abstractmethod
    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        pass

    @abstractmethod
    def stream(
        self,
        request: GenerateRequest,
    ) -> Generator[str, None, None]:
        pass