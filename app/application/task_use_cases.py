from app.domain.models import Task, TaskCreate, TaskUpdate
from app.domain.ports import TaskRepositoryPort
from app.domain.exceptions import TaskNotFoundError

class TaskService:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.list_tasks()

    def get_task_by_id(self, task_id: int) -> Task:
        try:
            return self.repository.get_task_by_id(task_id)
        except TaskNotFoundError:
            raise
    
    def create_task(self, task_create: TaskCreate) -> Task:
        return self.repository.create_task(task_create)

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        try:
            return self.repository.update_task(task_id, task_update)
        except TaskNotFoundError:
            raise

    def delete_task(self, task_id: int) -> None:
        try:
            self.repository.delete_task(task_id)
        except TaskNotFoundError:
            raise

    def list_pending_tasks(self) -> list[Task]:
        return self.repository.list_pending_tasks()