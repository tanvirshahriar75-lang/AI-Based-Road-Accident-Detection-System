from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def auth_headers():
    email = f"video-{uuid4().hex}@example.com"
    password = "StrongPass123"
    response = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert response.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_video_upload_rejects_non_video():
    headers = auth_headers()
    response = client.post("/api/v1/videos/upload", headers=headers, files={"file": ("note.txt", b"not a video", "text/plain")})
    assert response.status_code == 400


def test_video_endpoints_require_authentication():
    assert client.get("/api/v1/videos").status_code == 401


def test_video_not_found_is_scoped_to_user():
    headers = auth_headers()
    assert client.get("/api/v1/videos/999999", headers=headers).status_code == 404
    assert client.delete("/api/v1/videos/999999", headers=headers).status_code == 404
    assert client.post("/api/v1/videos/999999/process", headers=headers).status_code == 404
