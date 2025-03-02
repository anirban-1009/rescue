from fastapi.testclient import TestClient

def test_root(test_client: TestClient):
    """Test root endpoint returns welcome message."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Swift Response API"}

def test_adding_first_responder(test_client: TestClient):
    """Test adding a new first responder to the database."""
    first_responder_data = {
        "fullname": "John Doe",
        "email": "johndoe1@example.com",
        "designation": "Firefighter",
        "age": 35,
        "service": "Fire Department"
    }

    response = test_client.post("/firstResponder/create", json=first_responder_data)

    assert response.status_code == 200
    assert response.json()["fullname"] == "John Doe"
    assert response.json()["email"] == "johndoe@example.com"