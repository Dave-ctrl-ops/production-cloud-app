from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200


def test_update_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Task created for update test"
        }
    )

    assert create_response.status_code == 200

    task_id = create_response.json()[0]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Learn Kubernetes",
            "description": "Understand deployments and services",
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.json() == [
        task_id,
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


def test_delete_task():

    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Test Task",
            "description": "Task created for delete test"
        }
    )

    assert create_response.status_code == 200

    task_id = create_response.json()[0]

    response = client.delete(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 200
    assert response.json() == [
        task_id,
        "Delete Test Task",
        "Task created for delete test",
        False
    ]

    get_response = client.get("/tasks")

    task_ids = [task[0] for task in get_response.json()]

    assert task_id not in task_ids


def test_delete_task_not_found():

    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }