import pytest

from app.domain.models import Task, TaskCreate, TaskUpdate
from pydantic import ValidationError


def test_task_create_accepts_minimal_data():
    task_create = TaskCreate(title="Comprar leite")

    assert task_create.title == "Comprar leite"
    assert task_create.description is None
    assert task_create.completed is False


def test_task_model_includes_id_and_fields():
    task = Task(id=1, title="Fazer exercício", description="Corrida 5km", completed=True)

    assert task.id == 1
    assert task.title == "Fazer exercício"
    assert task.description == "Corrida 5km"
    assert task.completed is True


def test_task_update_allows_partial_data():
    task_update = TaskUpdate(description="Comprar pão", completed=True)

    assert task_update.title is None
    assert task_update.description == "Comprar pão"
    assert task_update.completed is True


def test_task_create_rejects_empty_title():
    with pytest.raises(ValidationError):
        TaskCreate(title="")
