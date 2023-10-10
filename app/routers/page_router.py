from typing import Annotated
from fastapi import APIRouter, Request, Form, Response, status
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import get_todos, create_todo, delete_todo

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    todos = get_todos()
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "num_todos": len(todos),
            "todos": todos
        }
    )


@router.get("/htmx/todo", response_class=HTMLResponse)
async def todo_fragment(request: Request):
    todos = get_todos()
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "num_todos": len(todos),
            "todos": todos
        },
        block_name="content"
    )


@router.post("/htmx/todo", response_class=HTMLResponse)
async def create_todo_fragment(request: Request, todo: Annotated[str, Form()]):
    todos = get_todos()
    create_todo(todo)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "num_todos": len(todos),
            "todos": todos
        },
        block_name="content"
    )


@router.delete("/htmx/todo/{id}")
async def delete_todo_fragment(request: Request, id: int):
    delete_todo(id)
    return Response(status_code=status.HTTP_200_OK)
