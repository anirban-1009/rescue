from fastapi.testclient import TestClient
from apps.backend.server.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to this fantastic app!"}

def test_adding_student():
    response = client.post("/student", json={
    "fullname": "string",
    "email": "user@example.com",
    "course_of_study": "string",
    "year": 1,
    "gpa": 4
    })

    assert response.status_code == 200