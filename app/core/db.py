todos = [{
    "name": "Walk the dog"
}, {
    "name": "buy groceries"
}, {
    "name": "wash the car"
}]


def get_todos():
    return todos


def create_todo(todo: str):
    todos.append({"name": todo})


def delete_todo(id: int):
    todos.remove(todos[id - 1])
    return todos
