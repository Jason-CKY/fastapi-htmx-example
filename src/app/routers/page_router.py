from typing import Annotated
from fastapi import APIRouter, Request, Form, Response, status
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import get_tasks

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    todos = await get_tasks()
    backlog, inProgress, done = [], [], []
    for todo in todos:
        if todo.status == "backlog":
            backlog.append(todo)
        elif todo.status == "progress":
            inProgress.append(todo)
        else:
            done.append(todo)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "backlog": backlog,
            "inProgress": inProgress,
            "done": done,
        },
    )


@router.get("/htmx/todo", response_class=HTMLResponse)
async def todo_fragment(request: Request):
    todos = get_tasks()
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
        block_name="content",
    )


@router.post("/htmx/todo", response_class=HTMLResponse)
async def create_todo_fragment(request: Request, todo: Annotated[str, Form()]):
    todos = get_tasks()
    # create_todo(todo)
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
        block_name="content",
    )


@router.delete("/htmx/todo/{id}")
async def delete_todo_fragment(request: Request, id: int):
    # delete_todo(id)
    return Response(status_code=status.HTTP_200_OK)
