from app.domain.models import Task, TaskCreate, TaskUpdate
from app.domain.ports import TaskRepositoryPort


class InMemoryTaskRepository(TaskRepositoryPort):
    def list_tasks(self):
        return []

    def get_task_by_id(self, task_id: int) -> Task:
        raise KeyError

    def create_task(self, task_create: TaskCreate) -> Task:
        return Task(id=1, **task_create.dict())

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        return Task(id=task_id, title=task_update.title or "Título", description=task_update.description, completed=task_update.completed if task_update.completed is not None else False)

    def delete_task(self, task_id: int) -> None:
        return None

    def list_pending_tasks(self):
        return []


def test_task_repository_port_can_be_implemented():
    repository = InMemoryTaskRepository()

    assert repository.list_tasks() == []
    assert repository.create_task(TaskCreate(title="Nova tarefa")).id == 1


def test_abstract_repository_cannot_be_instantiated_directly():
    try:
        TaskRepositoryPort()
        assert False, "TaskRepositoryPort should not be instantiable"
    except TypeError:
        assert True
