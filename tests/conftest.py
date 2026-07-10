"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

# Add project root to path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_collection_modifyitems(config, items):
    """Add asyncio marker to async tests automatically."""
    for item in items:
        if "asyncio" in item.keywords:
            continue
        if hasattr(item.obj, "_is_coroutine"):
            item.add_marker(pytest.mark.asyncio)
