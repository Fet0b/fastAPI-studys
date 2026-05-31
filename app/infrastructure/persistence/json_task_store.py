from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
import threading
from typing import List

from app.domain.models import Task, TaskCreate, TaskUpdate
from app.domain.exceptions import TaskNotFoundError
from app.domain.ports import TaskRepositoryPort


class JSONTaskStore(TaskRepositoryPort):
    """Repositório de tarefas persistido em arquivo JSON.

    - Armazena uma lista de tarefas como JSON.
    - Operações de escrita são atômicas (escreve em arquivo temporário e renomeia).
    - Protegido por `threading.Lock` para evitar corrida em ambiente single-process.
    """

    def __init__(self, path: str | Path = "data/tasks.json") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        # garante que exista o arquivo
        if not self._path.exists():
            self._write_data([])

    def _read_data(self) -> List[dict]:
        try:
            with self._path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[dict]) -> None:
        # escrita atômica: escreve em arquivo temporário na mesma pasta e move
        with NamedTemporaryFile("w", delete=False, dir=str(self._path.parent), encoding="utf-8") as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            tmp.flush()
            tmp_name = tmp.name
        Path(tmp_name).replace(self._path)

    def _load_tasks(self) -> List[Task]:
        raw = self._read_data()
        return [Task.parse_obj(item) for item in raw]

    def _dump_tasks(self, tasks: List[Task]) -> None:
        raw = [t.dict() for t in tasks]
        self._write_data(raw)

    def list_tasks(self) -> list[Task]:
        return self._load_tasks()

    def get_task_by_id(self, task_id: int) -> Task:
        tasks = self._load_tasks()
        for t in tasks:
            if t.id == task_id:
                return t
        raise TaskNotFoundError(task_id=task_id)

    def create_task(self, task_create: TaskCreate) -> Task:
        with self._lock:
            tasks = self._load_tasks()
            max_id = max((t.id for t in tasks), default=0)
            new_id = max_id + 1
            new_task = Task(id=new_id, **task_create.dict())
            tasks.append(new_task)
            self._dump_tasks(tasks)
            return new_task

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        with self._lock:
            tasks = self._load_tasks()
            for i, t in enumerate(tasks):
                if t.id == task_id:
                    updated_data = t.dict()
                    update_fields = task_update.dict(exclude_unset=True)
                    updated_data.update(update_fields)
                    updated = Task.parse_obj(updated_data)
                    tasks[i] = updated
                    self._dump_tasks(tasks)
                    return updated
            raise TaskNotFoundError(task_id=task_id)

    def delete_task(self, task_id: int) -> None:
        with self._lock:
            tasks = self._load_tasks()
            for i, t in enumerate(tasks):
                if t.id == task_id:
                    del tasks[i]
                    self._dump_tasks(tasks)
                    return None
            raise TaskNotFoundError(task_id=task_id)

    def list_pending_tasks(self) -> list[Task]:
        return [t for t in self._load_tasks() if not t.completed]
