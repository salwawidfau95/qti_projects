import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200

def test_login_user_success(client):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200

def test_login_user_fail(client):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
