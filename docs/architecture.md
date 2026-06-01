# Architecture Documentation

## Introduction

This document provides a technical overview of the project's architecture, design decisions, execution flow, and implementation details.

The project is a Task Management API built with FastAPI and organized using concepts inspired by Clean Architecture and Hexagonal Architecture.

The main goal is to separate business rules from infrastructure concerns, making the code easier to test, maintain, and evolve.

---

# High-Level Architecture

```text
Client
  │
  ▼
FastAPI Endpoints
  │
  ▼
TaskService
  │
  ▼
TaskRepositoryPort
  │
  ▼
JSONTaskStore
  │
  ▼
tasks.json
```

Each layer has a single responsibility.

---

# Layer Responsibilities

## Domain Layer

Location:

```text
app/domain/
```

The domain layer contains the core business concepts.

This layer must not depend on FastAPI, JSON storage, databases, or infrastructure concerns.

### Components

#### models.py

Defines the application's data structures.

##### TaskBase

Base model containing common task attributes.

```python
title
description
completed
```

##### TaskCreate

Represents data required to create a task.

##### TaskUpdate

Represents partial updates.

All fields are optional to support update operations.

##### Task

Represents a complete task entity including its identifier.

```python
id
title
description
completed
```

---

#### exceptions.py

Contains domain-specific exceptions.

##### DomainError

Base exception for all business-related errors.

##### TaskNotFoundError

Raised when a requested task cannot be found.

Example:

```python
raise TaskNotFoundError(task_id)
```

---

#### ports.py

Contains repository abstractions.

##### TaskRepositoryPort

Defines the contract that every repository implementation must follow.

Required operations:

```python
list_tasks()
get_task_by_id()
create_task()
update_task()
delete_task()
list_pending_tasks()
```

The domain only knows this contract.

It does not know how tasks are stored.

---

# Application Layer

Location:

```text
app/application/
```

The application layer coordinates business operations.

---

## task_use_cases.py

Contains the TaskService.

### Responsibilities

The service acts as the application's orchestration layer.

It sits between the API and the repository abstraction.

Current operations:

* List tasks
* Get task by ID
* Create task
* Update task
* Delete task
* List pending tasks

Current implementation mostly delegates calls to the repository.

Future business rules should be implemented here.

Examples:

* Duplicate title validation
* Authorization checks
* Auditing
* Notifications
* Event publishing

---

# Infrastructure Layer

Location:

```text
app/infrastructure/
```

Contains concrete technical implementations.

---

## persistence/json_task_store.py

Implements the repository contract using a JSON file.

```python
class JSONTaskStore(TaskRepositoryPort)
```

This class is the application's persistence adapter.

---

# Internal Components

## _read_data()

Reads raw JSON content from disk.

Returns:

```python
list[dict]
```

---

## _write_data()

Persists task data to disk.

Uses atomic replacement to avoid file corruption.

Process:

```text
Create temporary file
        │
        ▼
Write updated data
        │
        ▼
Replace original file
```

This approach minimizes the risk of data loss.

---

## Thread Safety

The repository uses:

```python
threading.Lock()
```

to prevent concurrent write operations.

This ensures consistency when multiple requests modify the JSON file simultaneously.

---

# CRUD Operations

## Create Task

Flow:

```text
Load tasks
    │
    ▼
Find highest ID
    │
    ▼
Generate next ID
    │
    ▼
Create Task object
    │
    ▼
Persist to JSON
```

---

## Update Task

Flow:

```text
Find task
    │
    ▼
Merge updated fields
    │
    ▼
Persist changes
```

Only supplied fields are modified.

---

## Delete Task

Flow:

```text
Find task
    │
    ▼
Remove task
    │
    ▼
Persist updated list
```

---

## List Pending Tasks

Filters tasks where:

```python
completed == False
```

---

# API Layer

Location:

```text
app/main.py
```

The API layer exposes the application's functionality through HTTP endpoints.

---

# Registered Endpoints

## Health Check

```http
GET /ping
```

Response:

```json
{
  "ok": true
}
```

---

## List Tasks

```http
GET /tasks
```

Returns all tasks.

---

## List Pending Tasks

```http
GET /tasks/pending
```

Returns only incomplete tasks.

---

## Get Task

```http
GET /tasks/{task_id}
```

Returns a single task.

Throws:

```python
TaskNotFoundError
```

if the task does not exist.

---

## Create Task

```http
POST /tasks
```

Creates a new task.

---

## Update Task

```http
PUT /tasks/{task_id}
```

Updates an existing task.

---

## Delete Task

```http
DELETE /tasks/{task_id}
```

Deletes a task.

---

# Error Handling

The project uses custom exceptions instead of generic exceptions.

Example:

```python
raise TaskNotFoundError(task_id)
```

Benefits:

* Better readability
* Better debugging
* More expressive business logic
* Easier HTTP error mapping

---

# Dependency Flow

The dependency direction follows:

```text
Domain
   ▲
   │
Application
   ▲
   │
Infrastructure
```

The domain defines abstractions.

The infrastructure implements those abstractions.

The application coordinates interactions between them.

This follows the Dependency Inversion Principle (DIP).

---

# Architectural Benefits

## Decoupling

Business rules do not depend on storage details.

---

## Testability

Repositories can be replaced by fake implementations during testing.

Example:

```python
FakeTaskRepository
```

without modifying the service layer.

---

## Extensibility

The JSON repository can be replaced with:

* SQLite
* PostgreSQL
* MySQL
* MongoDB

without changing the domain layer.

---

# Current Limitations

The current implementation intentionally remains simple.

Known limitations:

* JSON is not suitable for large datasets
* No authentication
* No authorization
* No database transactions
* No pagination
* No logging system
* No dependency injection container

---

# Future Improvements

Potential evolutions include:

* SQLAlchemy integration
* PostgreSQL support
* Docker deployment
* JWT authentication
* Structured logging
* Metrics and monitoring
* Repository factory
* Service interfaces
* Dedicated use case classes
* Event-driven architecture

---

# Conclusion

This project demonstrates how a simple CRUD API can be structured using architectural principles commonly found in larger production systems.

While the business domain remains intentionally simple, the organization of the code provides a foundation for studying:

* Clean Architecture
* Hexagonal Architecture
* Dependency Inversion
* Repository Pattern
* Domain Modeling
* FastAPI Development
