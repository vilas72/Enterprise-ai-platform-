from app.models.generate_request import GenerateRequest
from app.providers.mock_provider import MockProvider


def test_mock_provider():

    provider = MockProvider()

    request = GenerateRequest(
        prompt="Explain Kubernetes"
    )

    response = provider.generate(request)

    assert response.provider == "Mock"
    assert response.model == "mock-model-v1"
    assert response.response == "Mock Response: Explain Kubernetes"