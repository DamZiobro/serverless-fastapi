from typing import List

import pytest

from api.models.todo import TodoDTO
from api.repos.todo import (
    InMemoryTodoRepository,
    TodoInterface,
)


@pytest.fixture
def todo_repo() -> TodoInterface:
    repo = InMemoryTodoRepository()
    repo.todos = []  # clear persistance between each test
    return repo


def test_create_todo(todo_repo):
    todo = TodoDTO(task="Test task", description="Test description")
    created_todo = todo_repo.create_todo(todo)
    assert created_todo.task == todo.task
    assert created_todo.description == todo.description


def test_read_todos(todo_repo):
    todo1 = TodoDTO(task="Task 1", description="Description 1")
    todo2 = TodoDTO(task="Task 2", description="Description 2")
    todo_repo.create_todo(todo1)
    todo_repo.create_todo(todo2)
    todos = todo_repo.read_todos()
    assert isinstance(todos, List)
    assert len(todos) == 2
    assert todos[0].task == todo1.task
    assert todos[0].description == todo1.description
    assert todos[1].task == todo2.task
    assert todos[1].description == todo2.description


def test_read_todo_by_id(todo_repo):
    todo1 = TodoDTO(task="Task 1", description="Description 1")
    todo2 = TodoDTO(task="Task 2", description="Description 2")
    created_todo1 = todo_repo.create_todo(todo1)
    created_todo2 = todo_repo.create_todo(todo2)
    retrieved_todo1 = todo_repo.read_todo_by_id(created_todo1.id)
    assert retrieved_todo1.task == created_todo1.task
    assert retrieved_todo1.description == created_todo1.description
    retrieved_todo2 = todo_repo.read_todo_by_id(created_todo2.id)
    assert retrieved_todo2.task == created_todo2.task
    assert retrieved_todo2.description == created_todo2.description


def test_read_todo_by_id_not_found(todo_repo):
    unknown_id = 1
    todo = todo_repo.read_todo_by_id(unknown_id)
    assert todo is None


def test_update_todo_by_id(todo_repo):
    todo1 = TodoDTO(task="Task 1", description="Description 1")
    created_todo = todo_repo.create_todo(todo1)
    updated_todo = TodoDTO(task="New task", description="New description")
    updated_todo = todo_repo.update_todo_by_id(created_todo.id, updated_todo)
    assert updated_todo.task == "New task"
    assert updated_todo.description == "New description"
    retrieved_todo = todo_repo.read_todo_by_id(created_todo.id)
    assert retrieved_todo.task == "New task"
    assert retrieved_todo.description == "New description"


def test_update_todo_by_id_not_found(todo_repo):
    todo1 = TodoDTO(task="Task 1", description="Description 1")
    todo_repo.create_todo(todo1)
    updated_todo = TodoDTO(task="New task", description="New description")
    updated_todo = todo_repo.update_todo_by_id(123, updated_todo)
    assert updated_todo is None


def test_delete_todo_by_id(todo_repo):
    todo1 = TodoDTO(task="Task 1", description="Description 1")
    created_todo1 = todo_repo.create_todo(todo1)
    todo2 = TodoDTO(task="Task 2", description="Description 2")
    created_todo2 = todo_repo.create_todo(todo2)
    deleted = todo_repo.delete_todo_by_id(created_todo1.id)
    assert deleted is True
    todos = todo_repo.read_todos()
    assert len(todos) == 1
    assert todos[0].id == created_todo2.id


def test_delete_todo_by_id_not_found(todo_repo):
    unknown_id = 1
    deleted = todo_repo.delete_todo_by_id(unknown_id)
    assert deleted is False
