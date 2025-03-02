import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient
from server.app import app  # Import your FastAPI app
from server.data_utils.first_responder import FirstResponderHandler, BaseMongoHandler
class MockBaseMongoHandler(BaseMongoHandler):
    """Mock version of BaseMongoHandler that uses an in-memory database."""
    def __init__(self):
        self.client = MongoClient()  # In-memory MongoDB
        self.database = self.client["test_database"]

@pytest.fixture
def mock_db():
    """Fixture to create a mock MongoDB database."""
    client = MongoClient()
    db = client["test_database"]
    return db

@pytest.fixture
def mock_baseMongoHandler(mock_db):
    """Fixture to return a mocked BaseMongoHandler using an in-memory DB."""
    handler = MockBaseMongoHandler()
    handler.database = mock_db
    return handler

@pytest.fixture
def mock_firstResponderHandler(mock_baseMongoHandler):
    """Fixture to mock FirstResponderHandler with the mock DB."""
    handler = FirstResponderHandler()
    handler.database = mock_baseMongoHandler.database  # Override with mock DB
    handler.collection = handler.database["FirstResponder"]  # Override collection
    return handler

@pytest.fixture
def test_client(mock_db, mock_firstResponderHandler):
    """Override FastAPI dependencies and return a TestClient."""
    
    async def override_get_database():
        return mock_db

    async def override_firstResponderHandler():
        return mock_firstResponderHandler

    app.dependency_overrides[BaseMongoHandler] = lambda: mock_baseMongoHandler
    app.dependency_overrides[FirstResponderHandler] = override_firstResponderHandler

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()  # Cleanup after tests