from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import todos
import asyncio

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    _todos = []
    for i in range(len(todos)):
        _todos.append({"id": i + 1, "todo": todos[i]})

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "todos": _todos
        }
    )


@router.get("/todo", response_class=HTMLResponse)
async def get_todos(request: Request):
    _todos = []
    for i in range(len(todos)):
        _todos.append({"id": i + 1, "todo": todos[i]})
    await asyncio.sleep(1)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "todos": _todos
        },
        block_name="content"
    )


@router.post("/todo", response_class=HTMLResponse)
async def create_todo(request: Request, todo: Annotated[str, Form()]):
    todos.append(todo)
    _todos = []
    for i in range(len(todos)):
        _todos.append({"id": i + 1, "todo": todos[i]})
    await asyncio.sleep(1)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "todos": _todos
        },
        block_name="content"
    )
