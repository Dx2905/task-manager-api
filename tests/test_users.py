import pytest


@pytest.fixture(scope="module")
def user_auth_header(client):
    data = {"username": "user1", "email": "user1@example.com", "password": "test123"}
    client.post("/auth/signup", json=data)

    res = client.post("/auth/login", data={"username": data["email"], "password": data["password"]},
                      headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def admin_auth_header(client):
    admin_data = {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "adminpass"
    }
    # Create admin if doesn't exist
    client.post("/auth/signup", json=admin_data)

    # Force set admin role if not already
    from app.models.user import User
    from app.core.database import SessionLocal
    with SessionLocal() as db:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        admin.role = "admin"
        db.commit()

    login_res = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "adminpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_user_by_id(client, user_auth_header):
    # Get current user info
    me = client.get("/auth/me", headers=user_auth_header)
    assert me.status_code == 200
    user_id = me.json()["id"]

    # Retrieve same user by ID
    res = client.get(f"/users/{user_id}", headers=user_auth_header)
    assert res.status_code == 200
    assert res.json()["id"] == user_id
    assert res.json()["email"] == "user1@example.com"


def test_update_user(client, user_auth_header):
    me = client.get("/auth/me", headers=user_auth_header)
    user_id = me.json()["id"]

    update_data = {"username": "updated_user1"}
    res = client.put(f"/users/{user_id}", json=update_data, headers=user_auth_header)
    assert res.status_code == 200
    assert res.json()["username"] == "updated_user1"


def test_forbidden_user_access(client, user_auth_header):
    # Try accessing another user’s ID (e.g., ID = 9999)
    res = client.get("/users/9999", headers=user_auth_header)
    assert res.status_code in (403, 404)

def test_admin_can_delete_user(client, admin_auth_header):
    # Create a new user to be deleted
    user_data = {
        "username": "tempuser",
        "email": "tempuser@example.com",
        "password": "temp1234"
    }
    signup_res = client.post("/auth/signup", json=user_data)
    assert signup_res.status_code == 201
    user_id = signup_res.json()["id"]

    # Admin deletes user
    res = client.delete(f"/users/{user_id}", headers=admin_auth_header)
    assert res.status_code == 204

    # Confirm deletion
    get_res = client.get(f"/users/{user_id}", headers=admin_auth_header)
    assert get_res.status_code == 404
