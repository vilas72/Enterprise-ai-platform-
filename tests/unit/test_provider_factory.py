from app.bootstrap.provider_bootstrap import register_providers
from app.providers.provider_factory import ProviderFactory
from app.providers.mock_provider import MockProvider


register_providers()


def test_create_mock_provider():

    factory = ProviderFactory()

    provider = factory.create("mock")

    assert isinstance(provider, MockProvider)