from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    title: str
    description: str


todos = [
    {
        "id": 1,
        "title": "Walk the dog",
        "description": "test description 1",
        "status": "backlog",
    },
    {
        "id": 2,
        "title": "buy groceries",
        "description": "test description 2",
        "status": "backlog",
    },
    {
        "id": 3,
        "title": "wash the car",
        "description": "test description 3",
        "status": "backlog",
    },
    {
        "id": 4,
        "title": "test4",
        "description": "test description 1",
        "status": "in-progress",
    },
    {
        "id": 5,
        "title": "test5",
        "description": "test description 2",
        "status": "in-progress",
    },
    {
        "id": 6,
        "title": "test6",
        "description": "test description 3",
        "status": "in-progress",
    },
    {
        "id": 7,
        "title": "test7",
        "description": "test description 4 test test test",
        "status": "done",
    },
    {
        "id": 8,
        "title": "test8",
        "description": "test description 5 test test test",
        "status": "done",
    },
    {
        "id": 9,
        "title": "test9",
        "description": "test description 6 test test test",
        "status": "done",
    },
]


def get_todos():
    return todos


def create_todo(todo: Todo):
    todos.append(todo)


def delete_todo(id: int):
    for todo in todos:
        if todo["id"] == id:
            todos.remove(todo)
    return todos
