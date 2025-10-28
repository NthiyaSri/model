import os
from app import create_app


def test_products_list_empty_ok(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    app = create_app()
    client = app.test_client()
    rv = client.get("/api/products")
    assert rv.status_code == 200
    assert isinstance(rv.get_json(), list)
