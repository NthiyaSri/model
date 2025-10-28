import os
from app import create_app


def test_register_and_login(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    app = create_app()
    client = app.test_client()

    rv = client.post("/api/auth/register", json={"email": "u@test.com", "password": "secret123"})
    assert rv.status_code == 201

    rv = client.post("/api/auth/login", json={"email": "u@test.com", "password": "secret123"})
    assert rv.status_code == 200
    assert "token" in rv.get_json()
