from locust import (
    HttpUser,
    between,
    task,
)

from api.models.todo import TodoDTO


class TodoUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_todo(self):
        self.client.post(
            "/todos", json=TodoDTO(task="Test task", completed=False).dict()
        )

    @task
    def read_todos(self):
        self.client.get("/todos")

    @task
    def read_todo(self):
        self.client.get("/todos/1")

    @task
    def update_todo(self):
        self.client.put(
            "/todos/1", json=TodoDTO(task="Test task updated", completed=True).dict()
        )
