from app.bootstrap.provider_bootstrap import register_providers
from app.providers.provider_factory import ProviderFactory
from app.services.ai_service import AIService
from app.models.generate_request import GenerateRequest


register_providers()


def test_generate_response():

    factory = ProviderFactory()

    service = AIService(factory)

    request = GenerateRequest(
        provider_name="mock",
        prompt="Hello AI"
    )

    response = service.generate(request)

    assert response.provider == "Mock"
    assert response.model == "mock-model-v1"
    assert response.response == "Mock Response: Hello AI"