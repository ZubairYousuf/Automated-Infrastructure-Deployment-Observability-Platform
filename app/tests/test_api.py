from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").json() == {"status": "ready"}

def test_root():
    assert client.get("/").json()["status"] == "running"

def test_task_round_trip():
    response = client.post("/api/v1/tasks", json={"title": "ship release"})
    assert response.status_code == 201
    task = response.json()
    assert client.get(f"/api/v1/tasks/{task['id']}").json() == task
    assert any(t["id"] == task["id"] for t in client.get("/api/v1/tasks").json()["items"])

def test_invalid_task():
    assert client.post("/api/v1/tasks", json={"title": ""}).status_code == 422

def test_unknown_task():
    assert client.get("/api/v1/tasks/missing").status_code == 404

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "cloudops_http_requests_total" in response.text

def test_unready(monkeypatch):
    monkeypatch.setenv("FORCE_UNREADY", "1")
    assert client.get("/health/ready").status_code == 503
