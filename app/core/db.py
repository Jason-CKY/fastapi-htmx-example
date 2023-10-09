todos = [
    "Walk the dog",
    "Buy groceries",
    "Wash the car",
]


def get_todos():
    _todos = []
    for i in range(len(todos)):
        _todos.append({"id": i + 1, "todo": todos[i]})
    return _todos

def create_todo(todo: str):
    todos.append(todo)
