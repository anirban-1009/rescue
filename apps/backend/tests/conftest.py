# tests/conftest.py
import pytest
import asyncio

# This is needed for async tests with pytest
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()