from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, description="Título da tarefa")
    description: Optional[str] = Field(None, description="Descrição opcional da tarefa")
    completed: bool = Field(False, description="Marca se a tarefa está concluída")


class TaskCreate(TaskBase):
    """Dados necessários para criar uma nova tarefa."""


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Título atualizado da tarefa")
    description: Optional[str] = Field(None, description="Descrição atualizada da tarefa")
    completed: Optional[bool] = Field(None, description="Flag de conclusão atualizada")


class Task(TaskBase):
    id: int = Field(..., description="Identificador único da tarefa")

    class Config:
        orm_mode = True
