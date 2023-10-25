from typing import Annotated
from fastapi import APIRouter, Request, Form, Response, status
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import get_tasks, create_task
import shortuuid


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    tasks = await get_tasks()
    backlog, inProgress, done = [], [], []
    for task in tasks:
        if task.status == "backlog":
            backlog.append(task)
        elif task.status == "progress":
            inProgress.append(task)
        else:
            done.append(task)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "backlog": backlog,
            "inProgress": inProgress,
            "done": done,
        },
    )


@router.post("/htmx/task", response_class=HTMLResponse)
async def create_task_fragment(request: Request):
    return templates.TemplateResponse(
        "components/edit_task.html",
        {
            "request": request,
            "id": shortuuid.random(length=15),
        },
    )


@router.put("/htmx/task/{id}", response_class=HTMLResponse)
async def update_task_fragment(request: Request, id: str):
    task = await create_task(
        title="backend test title",
        description="backend_test_title",
        status="progress",
        id=id,
    )
    return templates.TemplateResponse(
        "components/new_task.html",
        {"request": request, "task": task},
    )


@router.delete("/htmx/task/{id}", response_class=HTMLResponse)
async def delete_task_fragment(request: Request, id: str):
    return ""
