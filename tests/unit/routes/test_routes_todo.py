import pytest
from fastapi.testclient import TestClient
from hypothesis import (
    HealthCheck,
    example,
    given,
    settings,
)
from hypothesis.strategies import (
    integers,
    text,
)

from api.main import app
from api.models.todo import (
    TodoDTO,
    TodoModel,
)
from api.repos.todo import (
    InMemoryTodoRepository,
    TodoInterface,
)
from api.routes.todo import create_todo_repository


# Suppress the function_scoped_fixture health check


@pytest.fixture
def todo_repository() -> TodoInterface:
    repo = InMemoryTodoRepository()
    repo.todos = []  # clear persistance between each test
    return repo


@pytest.fixture
def client(todo_repository: TodoInterface, monkeypatch) -> TestClient:
    app.dependency_overrides[create_todo_repository] = lambda: todo_repository
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_todo_repository():
    todo_repository = create_todo_repository()
    assert isinstance(todo_repository, InMemoryTodoRepository)


# Test create_todo_handler
@given(text(min_size=1, max_size=50), text(min_size=1, max_size=50))
@example("title", "description")
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_create_todo_handler_returns_201(
    client: TestClient, todo_repository: TodoInterface, monkeypatch, title, desc
):
    # Test case: create a new Todo successfully
    new_todo = TodoDTO(task=title, description=desc)
    created_todo = TodoModel(id=1, task=title, description=desc)
    monkeypatch.setattr(todo_repository, "create_todo", lambda todo: created_todo)

    response = client.post("/todos/", json=new_todo.dict())
    assert response.status_code == 201
    assert response.json() == created_todo.dict()


@given(text(min_size=1, max_size=50))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_create_todo_handler_validates_missing_input_fields(
    client: TestClient, todo_repository: TodoInterface, monkeypatch, desc
):
    # Test case: create a new Todo with missing required fields
    response = client.post("/todos/", json={"description": desc})
    assert response.status_code == 422


@given(integers(min_value=1))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_create_todo_handler_validates_incorrect_type_of_input_field(
    client: TestClient, todo_repository: TodoInterface, monkeypatch, int_value
):
    # Test case: create a new Todo with invalid input type
    invalid_todo = {"description": int_value}
    monkeypatch.setattr(todo_repository, "create_todo", lambda todo: invalid_todo)

    response = client.post("/todos/", json=invalid_todo)
    assert response.status_code == 422


# Test update_todo_handler
@given(text(min_size=1, max_size=50), text(min_size=1, max_size=50))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_update_todo_handler(
    client: TestClient,
    todo_repository: TodoInterface,
    monkeypatch,
    updated_title,
    updated_desc,
):
    # Test case: update an existing Todo successfully
    existing_todo = TodoModel(id=1, task="test task", description="test description")
    updated_todo = TodoModel(id=1, task=updated_title, description=updated_desc)
    monkeypatch.setattr(
        todo_repository, "update_todo_by_id", lambda id, todo: updated_todo
    )

    response = client.put(f"/todos/{existing_todo.id}", json=updated_todo.dict())
    assert response.status_code == 200
    assert response.json() == updated_todo.dict()


@given(text(min_size=1, max_size=50), text(min_size=1, max_size=50))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_update_todo_handler_returns_404_for_non_existing_todos(
    client: TestClient,
    todo_repository: TodoInterface,
    monkeypatch,
    updated_title,
    updated_desc,
):
    # Test case: update a non-existing Todo
    updated_todo = TodoModel(id=1, task=updated_title, description=updated_desc)
    non_existing_todo_id = 2
    monkeypatch.setattr(todo_repository, "update_todo_by_id", lambda id, todo: None)

    response = client.put(f"/todos/{non_existing_todo_id}", json=updated_todo.dict())
    assert response.status_code == 404


@given(text(min_size=1, max_size=50), text(min_size=1, max_size=50))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_read_todo_handler(client, todo_repository, monkeypatch, title, desc):
    # Arrange
    todo = TodoModel(id=1, task=title, description=desc)
    monkeypatch.setattr(todo_repository, "read_todo_by_id", lambda todo_id: todo)

    # Act
    response = client.get("/todos/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == todo.dict()


def test_read_todo_handler_not_found(client, todo_repository, monkeypatch):
    # Arrange
    monkeypatch.setattr(todo_repository, "read_todo_by_id", lambda todo_id: None)

    # Act
    response = client.get("/todos/1")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo_handler(client, todo_repository, monkeypatch):
    # Arrange
    monkeypatch.setattr(todo_repository, "delete_todo_by_id", lambda todo_id: True)

    # Act
    response = client.delete("/todos/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted successfully"}


def test_delete_todo_handler_not_found(client, todo_repository, monkeypatch):
    # Arrange
    monkeypatch.setattr(todo_repository, "delete_todo_by_id", lambda todo_id: False)

    # Act
    response = client.delete("/todos/1")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo 1 not found"}


@given(
    text(min_size=1, max_size=50),
    text(min_size=1, max_size=50),
    text(min_size=1, max_size=50),
    text(min_size=1, max_size=50),
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=10)
def test_read_todos(
    client: TestClient,
    todo_repository: InMemoryTodoRepository,
    monkeypatch,
    title1,
    desc1,
    title2,
    desc2,
):
    # Define test data
    test_todo_1 = TodoModel(id=1, task=title1, description=desc1)
    test_todo_2 = TodoModel(id=2, task=title2, description=desc2)

    # Mock the read_todos method to return test data
    monkeypatch.setattr(
        todo_repository, "read_todos", lambda: [test_todo_1, test_todo_2]
    )

    # Call the API endpoint
    response = client.get("/todos/")

    # Assert the response
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["task"] == test_todo_1.task
    assert response.json()[1]["description"] == test_todo_2.description
