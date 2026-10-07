import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import pytest
from app import create_app

@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("DEMO_API_KEY", "test-only-key")
    return create_app(str(tmp_path / "notes.db"))

@pytest.fixture
def client(app):
    return app.test_client()

KEY = {"X-API-Key": "test-only-key"}

def test_notes_crud_and_persistence(app, client):
    response = client.post("/api/notes", json={"text": " first note "}, headers=KEY)
    assert response.status_code == 201
    note_id = response.json["id"]
    restarted = create_app(app.config["DATABASE"]).test_client()
    assert restarted.get("/api/notes").json == [{"id": note_id, "text": "first note"}]
    assert client.delete(f"/api/notes/{note_id}", headers=KEY).status_code == 204
    assert client.get("/api/notes").json == []
    assert client.delete(f"/api/notes/{note_id}", headers=KEY).status_code == 404

@pytest.mark.parametrize("body", [{}, [], {"text": " "}, {"text": 123}, {"text": "x" * 501}])
def test_invalid_input(client, body):
    assert client.post("/api/notes", json=body, headers=KEY).status_code == 400

def test_auth_and_secret_not_disclosed(client, monkeypatch):
    assert client.post("/api/notes", json={"text": "a"}).status_code == 401
    assert client.delete("/api/notes/1").status_code == 401
    assert b"test-only-key" not in client.get("/api/config").data
    monkeypatch.delenv("DEMO_API_KEY")
    assert client.post("/api/notes", json={"text": "a"}, headers=KEY).status_code == 401

def test_sql_is_data(client):
    text = "'); DROP TABLE notes; --"
    assert client.post("/api/notes", json={"text": text}, headers=KEY).status_code == 201
    assert client.get("/api/notes").json[0]["text"] == text

def test_health_and_readiness_failure(app, client):
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200
    with sqlite3.connect(app.config["DATABASE"]) as db:
        db.execute("DROP TABLE notes")
    assert client.get("/readyz").status_code == 503
    assert client.get("/healthz").status_code == 200

def test_metrics_and_request_ids(client):
    a, b = client.get("/"), client.get("/missing")
    assert a.status_code == 200 and b.status_code == 404
    assert a.headers["X-Request-ID"] != b.headers["X-Request-ID"]
    assert b"notes_requests_total" in client.get("/metrics").data
    assert client.get("/work").json["completed"] is True

def test_parallel_writes(app):
    def insert(number):
        with app.test_client() as client:
            return client.post("/api/notes", json={"text": str(number)}, headers=KEY).status_code
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert list(pool.map(insert, range(12))) == [201] * 12
    assert len(app.test_client().get("/api/notes").json) == 12
