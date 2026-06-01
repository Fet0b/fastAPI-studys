# fastAPI-studys

# FastAPI Studies

A study project focused on building a clean, maintainable, and testable REST API using FastAPI and architectural patterns inspired by Clean Architecture and Hexagonal Architecture.

## Overview

This project implements a simple Task Management API while exploring software design principles such as:

* Separation of concerns
* Dependency inversion
* Repository pattern
* Domain-driven organization
* Error handling
* Automated testing
* API design with FastAPI

Although the business domain is intentionally simple, the project structure aims to simulate how larger applications can be organized and scaled.

## Architecture

The application is organized into distinct layers:

```text
app/
├── application/
│   └── task_use_cases.py
│
├── domain/
│   ├── exceptions.py
│   ├── models.py
│   └── ports.py
│
├── infrastructure/
│   └── persistence/
│       └── json_task_store.py
│
└── main.py
```

### Domain Layer

Contains the core business definitions and contracts.

#### Models

Defines the application's entities and data structures:

* `Task`
* `TaskCreate`
* `TaskUpdate`

#### Ports

Defines repository contracts used by the application layer.

Example:

```python
class TaskRepositoryPort(ABC):
    ...
```

The domain does not know how data is stored; it only knows which operations must be available.

#### Exceptions

Custom domain exceptions:

* `DomainError`
* `TaskNotFoundError`

---

### Application Layer

Contains the use cases and application services.

#### TaskService

Acts as the application's orchestration layer, coordinating interactions between the API and the repository abstraction.

Responsibilities include:

* Listing tasks
* Creating tasks
* Updating tasks
* Deleting tasks
* Retrieving pending tasks

The service depends on abstractions rather than concrete implementations.

---

### Infrastructure Layer

Contains technical implementations and persistence details.

#### JSONTaskStore

Implements the `TaskRepositoryPort` contract using a JSON file as the storage backend.

Features:

* Persistent storage
* Thread-safe writes
* Atomic file replacement
* Repository pattern implementation

Because the application depends on the repository interface, the storage backend can be replaced with SQLite, PostgreSQL, MongoDB, or any other persistence mechanism without modifying the business logic.

---

### API Layer

The FastAPI application exposes REST endpoints for task management.

Available endpoints:

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| GET    | `/ping`          | Health check            |
| GET    | `/tasks`         | List all tasks          |
| GET    | `/tasks/pending` | List pending tasks      |
| GET    | `/tasks/{id}`    | Retrieve a task by ID   |
| POST   | `/tasks`         | Create a new task       |
| PUT    | `/tasks/{id}`    | Update an existing task |
| DELETE | `/tasks/{id}`    | Delete a task           |

---

## Running the Project

### Clone the Repository

```bash
git clone <repository-url>
cd fastAPI-studys
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Linux/macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Testing

Run the test suite with:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

---

## Design Goals

This project was created as a learning environment to explore:

* FastAPI development
* API design
* Clean code practices
* Dependency inversion
* Repository abstractions
* Domain-driven organization
* Testability
* Maintainability

The goal is not to build a production-ready task manager, but to understand how scalable software architecture can be applied even to small applications.

---

## Future Improvements

Possible next steps include:

* SQLite/PostgreSQL support
* SQLAlchemy integration
* Authentication and authorization
* Dependency injection container
* Docker support
* CI/CD pipeline
* Structured logging
* Metrics and observability
* Domain events
* Service interfaces and use-case separation

---

## License

This project is intended for educational and experimentation purposes.


"""
API simples de tarefas usando FastAPI.

Objetivo do exercício:
- Entender como uma API recebe requisições HTTP.
- Entender como criar rotas com FastAPI.
- Entender como enviar e receber dados em JSON.
- Entender como validar dados usando Pydantic.
- Entender os métodos HTTP principais: GET, POST, PUT e DELETE.

Requisitos da API:
1. Listar todas as tarefas.
2. Buscar uma tarefa pelo ID.
3. Criar uma nova tarefa.
4. Atualizar uma tarefa existente.
5. Deletar uma tarefa.
6. Listar apenas tarefas pendentes.

Como rodar:
1. Instale as dependências:
   pip install fastapi uvicorn

2. Rode o servidor:
   uvicorn main:app --reload

3. Abra a documentação automática:
   http://127.0.0.1:8000/docs
"""