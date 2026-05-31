from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.infrastructure.persistence.json_task_store import JSONTaskStore
from app.application.task_use_cases import TaskService
from app.domain.exceptions import TaskNotFoundError
from app.domain.models import Task, TaskCreate, TaskUpdate

app = FastAPI()
repo = JSONTaskStore("data/tasks.json")
service = TaskService(repository=repo)

@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(_: object, exc: TaskNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.get("/ping")
def ping() -> dict[str, bool]:
    return {"ok": True}

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return service.list_tasks()

@app.get("/tasks/pending", response_model=list[Task])
def list_pending_tasks() -> list[Task]:
    return service.list_pending_tasks()

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    return service.get_task_by_id(task_id)

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_create: TaskCreate) -> Task:
    return service.create_task(task_create)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    return service.update_task(task_id, task_update)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    service.delete_task(task_id)
    return None
