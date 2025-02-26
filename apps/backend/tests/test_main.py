from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Swift Response API"
    }

def test_adding_student():
    response = client.post("/firstResponder", json={
        "fullname": "John Doe",
        "email": "johndoe@example.com",
        "designation": "Firefighter",
        "age": 35,
        "service": "Fire Department"
    })

    assert response.status_code == 200