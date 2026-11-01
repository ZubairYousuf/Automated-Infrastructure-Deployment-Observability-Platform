"""Small instrumented API used to demonstrate delivery and observability."""
from __future__ import annotations
import os
import time
import uuid
from threading import Lock
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI(title="CloudOps Demo API", version="1.0.0")
REQUEST_COUNT = Counter("cloudops_http_requests_total", "Requests received by the API", ["method", "path", "status"])
REQUEST_DURATION = Histogram("cloudops_http_request_duration_seconds", "HTTP request duration", ["method", "path"])
_tasks: dict[str, dict[str, str]] = {}
_tasks_lock = Lock()

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)
    started = time.monotonic()
    try:
        response = await call_next(request)
    except Exception:
        REQUEST_COUNT.labels(request.method, "unhandled", "500").inc()
        REQUEST_DURATION.labels(request.method, "unhandled").observe(time.monotonic() - started)
        raise
    route = request.scope.get("route")
    path = getattr(route, "path", "unknown")
    REQUEST_COUNT.labels(request.method, path, str(response.status_code)).inc()
    REQUEST_DURATION.labels(request.method, path).observe(time.monotonic() - started)
    return response

@app.get("/")
def index():
    return {"name": "CloudOps Demo API", "version": "1.0.0", "status": "running"}

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    return {"status": "ready"} if os.getenv("FORCE_UNREADY") != "1" else Response(status_code=503)

@app.post("/api/v1/tasks", status_code=201)
def create_task(payload: TaskCreate):
    task_id = str(uuid.uuid4())
    task = {"id": task_id, "title": payload.title, "status": "pending"}
    with _tasks_lock:
        _tasks[task_id] = task
    return task

@app.get("/api/v1/tasks")
def list_tasks():
    with _tasks_lock:
        return {"items": list(_tasks.values()), "count": len(_tasks)}

@app.get("/api/v1/tasks/{task_id}")
def get_task(task_id: str):
    with _tasks_lock:
        task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
