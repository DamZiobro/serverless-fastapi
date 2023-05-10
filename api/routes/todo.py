"""Implementation of Use Cases based on the Clean Architecture principles"""

from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from api.models.todo import (
    TodoDTO,
    TodoModel,
)
from api.repos.todo import InMemoryTodoRepository


router = APIRouter(tags=["todos"])


def create_todo_repository():
    # Create an empty list to hold our Todo items
    return InMemoryTodoRepository()


# Create a Todo
@router.post("/todos", response_model=TodoModel, status_code=201)
async def create_todo_handler(
    todo: TodoDTO, todo_repository=Depends(create_todo_repository)
):
    todo = todo_repository.create_todo(todo)
    return todo


# Read all Todos
@router.get("/todos", response_model=List[TodoModel])
async def read_todos_handler(todo_repository=Depends(create_todo_repository)):
    return todo_repository.read_todos()


# Read a single Todo by ID
@router.get("/todos/{todo_id}", response_model=TodoModel)
async def read_todo_handler(
    todo_id: int, todo_repository=Depends(create_todo_repository)
):
    todo = todo_repository.read_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# Update a Todo
@router.put("/todos/{todo_id}", response_model=TodoModel)
async def update_todo_handler(
    todo_id: int, todo: TodoDTO, todo_repository=Depends(create_todo_repository)
):
    todo = todo_repository.update_todo_by_id(todo_id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id}not found")
    return todo


# Delete a Todo
@router.delete("/todos/{todo_id}")
async def delete_todo_handler(
    todo_id: int, todo_repository=Depends(create_todo_repository)
):
    deleted: bool = todo_repository.delete_todo_by_id(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return {"message": "Todo deleted successfully"}
