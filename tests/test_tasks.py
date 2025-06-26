import pytest

@pytest.fixture(scope="module")
def auth_header(client):
    signup_data = {
        "username": "taskuser",
        "email": "taskuser@example.com",
        "password": "testpass123"
    }
    client.post("/auth/signup", json=signup_data)

    login_res = client.post(
        "/auth/login",
        data={"username": "taskuser@example.com", "password": "testpass123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )


    assert login_res.status_code == 200, f"Login failed: {login_res.json()}"
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def created_task_id(client, auth_header):
    task_data = {"title": "Test Task", "description": "A task", "is_completed": False}
    res = client.post("/tasks/", json=task_data, headers=auth_header)
    assert res.status_code == 201
    return res.json()["id"]

def test_create_task(client, auth_header):
    task_data = {"title": "Another Task", "description": "Extra", "is_completed": False}
    res = client.post("/tasks/", json=task_data, headers=auth_header)
    assert res.status_code == 201
    assert res.json()["title"] == "Another Task"

def test_get_task_by_id(client, auth_header, created_task_id):
    res = client.get(f"/tasks/{created_task_id}", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["id"] == created_task_id

def test_get_all_tasks(client, auth_header):
    res = client.get("/tasks/?limit=10&offset=0", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_update_task(client, auth_header, created_task_id):
    update = {"title": "Updated Task", "description": "Updated", "is_completed": True}
    res = client.put(f"/tasks/{created_task_id}", json=update, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["is_completed"] is True

def test_delete_task(client, auth_header, created_task_id):
    res = client.delete(f"/tasks/{created_task_id}", headers=auth_header)
    assert res.status_code == 204

def test_get_deleted_task(client, auth_header, created_task_id):
    res = client.get(f"/tasks/{created_task_id}", headers=auth_header)
    assert res.status_code == 404
