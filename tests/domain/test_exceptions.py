from app.domain.exceptions import DomainError, TaskNotFoundError


def test_domain_error_stores_message_and_context():
    error = DomainError("Erro de domínio", foo="bar")

    assert str(error) == "Erro de domínio"
    assert error.context == {"foo": "bar"}


def test_task_not_found_error_contains_task_id():
    error = TaskNotFoundError(task_id=42)

    assert str(error) == "Tarefa com id 42 não encontrada."
    assert error.task_id == 42
    assert error.context["task_id"] == 42
