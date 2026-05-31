from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from .models import Task, TaskCreate, TaskUpdate


class TaskRepositoryPort(ABC):
    """Porta de repositório para tarefas no domínio."""

    @abstractmethod
    def list_tasks(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_task_by_id(self, task_id: int) -> Task:
        raise NotImplementedError

    @abstractmethod
    def create_task(self, task_create: TaskCreate) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_pending_tasks(self) -> list[Task]:
        raise NotImplementedError
