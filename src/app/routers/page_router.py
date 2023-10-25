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


@router.post("/htmx/todo/backlog", response_class=HTMLResponse)
async def create_todo_fragment(request: Request):
    return templates.TemplateResponse(
        "components/task.html",
        {"request": request, "title": "EMPTY", "description": "FILL IN"},
    )


@router.post("/htmx/todo/progress", response_class=HTMLResponse)
async def create_todo_fragment(request: Request):
    return templates.TemplateResponse(
        "components/task.html",
        {"request": request, "title": "test", "description": "FILL IN"},
    )


@router.post("/htmx/todo/done", response_class=HTMLResponse)
async def create_todo_fragment(request: Request):
    return templates.TemplateResponse(
        "components/task_done.html",
        {"request": request, "title": "TEST", "description": "FILL IN"},
    )
