from app.domain.generate_request import GenerateRequest
from app.providers.gemini_provider import GeminiProvider


def test_gemini_provider():

    provider = GeminiProvider()

    request = GenerateRequest(
        prompt="Explain what Retrieval-Augmented Generation is in 5 lines."
    )

    response = provider.generate(request)

    print(response)

    assert response.provider == "Gemini"
    assert response.response