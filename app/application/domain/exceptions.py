from __future__ import annotations

from typing import Any


class DomainError(Exception):
    """Exceção base para erros de domínio."""
    def __init__(self, message: str, **context: Any) -> None:
        super().__init__(message)
        self.context = context


class TaskNotFoundError(DomainError):
    """Tarefa não encontrada no repositório."""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"Tarefa com id {task_id} não encontrada.", task_id=task_id)
        self.task_id = task_id
