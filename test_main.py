from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200


def test_update_task():
    response = client.put(
        "/tasks/4",
        json={
            "title": "Learn Kubernetes",
            "description": "Understand deployments and services",
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.json() == [
        4,
        "Learn Kubernetes",
        "Understand deployments and services",
        True
    ]


def test_update_task_not_found():
    response = client.put(
        "/tasks/999",
        json={
            "title": "Test",
            "description": "Should not exist",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }