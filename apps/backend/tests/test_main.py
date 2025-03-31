import pytest
from fastapi.testclient import TestClient
from src.main import app  # Ensure this matches your actual file structure


@pytest.fixture
def test_client():
    """Fixture to provide a test client for FastAPI."""
    return TestClient(app)


def test_read_root(test_client):
    """Test the root endpoint ("/")."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Rescue API"}
