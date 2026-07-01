from app.core.config import settings

def test_default_provider():
    assert settings.default_provider == "gemini"

def test_app_name():
    assert settings.app_name == "Enterprise AI Platform"