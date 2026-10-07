from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_login_and_me():
    email = f"test-{uuid4().hex}@example.com"
    register = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "StrongPass123",
        "full_name": "Test User",
    })
    assert register.status_code == 201
    assert register.json()["email"] == email
    assert "hashed_password" not in register.json()

    login = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "StrongPass123",
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert token

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email


def test_duplicate_registration_is_rejected():
    email = f"duplicate-{uuid4().hex}@example.com"
    payload = {"email": email, "password": "StrongPass123"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409


def test_invalid_login_is_rejected():
    email = f"invalid-{uuid4().hex}@example.com"
    client.post("/api/v1/auth/register", json={"email": email, "password": "StrongPass123"})
    response = client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPass123"})
    assert response.status_code == 401
