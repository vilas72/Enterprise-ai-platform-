from app.domain.generate_request import GenerateRequest
from app.providers.openai_provider import OpenAIProvider


def test_openai_provider():

    provider = OpenAIProvider()

    request = GenerateRequest(
        prompt="Explain what Retrieval-Augmented Generation is in 5 lines."
    )

    response = provider.generate(request)

    print(response)

    assert response.provider == "OpenAI"
    assert response.response