from fastapi import FastAPI
from app.infrastructure.persistence.json_task_store import JSONTaskStore
from app.application.crud_https import TaskService
from app.domain.models import TaskCreate

app = FastAPI()
repo = JSONTaskStore("data/tasks.json")
service = TaskService(repository=repo)

@app.get("/ping")
def ping():
    return {"ok": True}

# exemplo de rota que cria uma tarefa
@app.post("/tasks")
def create_task(payload: dict):
    t = service.create_task(TaskCreate(**payload))
    return t