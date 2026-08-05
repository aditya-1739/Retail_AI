from app.db import models

def test_auth_flows(client):
    # 1. Register User
    register_payload = {
        "email": "auth@example.com",
        "password": "securepassword",
        "full_name": "Auth Test User",
        "role": "User"
    }
    response = client.post("/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "auth@example.com"
    assert data["full_name"] == "Auth Test User"
    assert data["role"] == "User"

    # 2. Login User
    login_payload = {
        "username": "auth@example.com",
        "password": "securepassword"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
