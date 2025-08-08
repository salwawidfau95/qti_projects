import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_user_get_own_profile(client, user_token_headers):
    response = client.get("/users/profile", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
    assert response.json()["username"] == "normaluser"

def test_user_update_own_profile(client, user_token_headers):
    payload = {
        "username": "updateduser",
        "email": "updated@example.com",
        "password": "newpassword123"
    }
    response = client.patch("/users/profile", headers=user_token_headers, json=payload)
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "updateduser"
    assert response.json()["user"]["email"] == "updated@example.com"

def test_user_delete_self(client, user_token_headers):
    response = client.delete("/users/profile", headers=user_token_headers)
    assert response.status_code in [200, 204]

