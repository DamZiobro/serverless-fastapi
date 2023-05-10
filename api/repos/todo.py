"""Implementation of Repositories based on the Clean Architecture principles"""

from abc import (
    ABC,
    abstractmethod,
)

from api.models.todo import (
    TodoDTO,
    TodoModel,
)


# Define a Todo interface
class TodoInterface(ABC):
    @abstractmethod
    def create_todo(self, todo: TodoDTO) -> TodoModel:
        pass

    @abstractmethod
    def read_todos(self) -> list:
        pass

    @abstractmethod
    def read_todo_by_id(self, todo_id: int) -> TodoModel:
        pass

    @abstractmethod
    def update_todo_by_id(self, todo_id: int, todo: TodoDTO) -> TodoModel:
        pass

    @abstractmethod
    def delete_todo_by_id(self, todo_id: int) -> bool:
        pass


TODOS_PERSISTANCE = []


# Define a Todo repository
class InMemoryTodoRepository(TodoInterface):
    def __init__(self):
        global TODOS_PERSISTANCE
        self.todos = TODOS_PERSISTANCE
        self.id = self.todos[-1].id if self.todos else 0

    def create_todo(self, todo: TodoDTO) -> TodoModel:
        self.id += 1
        new_todo = TodoModel(id=self.id, task=todo.task, description=todo.description)
        self.todos.append(new_todo)
        return new_todo

    def read_todos(self) -> list:
        return self.todos

    def read_todo_by_id(self, todo_id: int) -> TodoModel:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo_by_id(self, todo_id: int, todo: TodoDTO) -> TodoModel:
        for index, todo_item in enumerate(self.todos):
            if todo_item.id == todo_id:
                updated_todo = todo_item.copy(update=todo.dict())
                self.todos[index] = updated_todo
                return updated_todo
        return None

    def delete_todo_by_id(self, todo_id: int) -> bool:
        for index, todo_item in enumerate(self.todos):
            if todo_item.id == todo_id:
                self.todos.pop(index)
                return True
        return False
