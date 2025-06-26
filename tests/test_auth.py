def test_signup_and_login(client):
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }

    # Signup
    response = client.post("/auth/signup", json=signup_data)
    assert response.status_code == 201
    assert response.json()["email"] == signup_data["email"]

    # Login
    login_data = {
        "username": signup_data["email"],
        "password": signup_data["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
