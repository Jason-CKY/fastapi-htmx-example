from typing import Annotated
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import get_tasks, create_task, delete_task, get_task_by_id, update_task
from app.schemas.tasks import TaskStatus
from loguru import logger
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


@router.post("/htmx/task/empty/{status}", response_class=HTMLResponse)
async def create_empty_task_fragment(request: Request, status: TaskStatus):
    return templates.TemplateResponse(
        "components/edit_task.html",
        {
            "request": request,
            "id": shortuuid.random(length=15),
            "status": status.value,
            "title": "",
            "description": "",
        },
    )


@router.post("/htmx/task/{id}", response_class=HTMLResponse)
async def create_existing_task_fragment(request: Request, id: str):
    task = await get_task_by_id(id)
    return templates.TemplateResponse(
        "components/edit_task.html",
        {
            "request": request,
            "id": task.id,
            "status": task.status.value,
            "title": task.title,
            "description": task.description,
        },
    )


@router.put("/htmx/task/{id}", response_class=HTMLResponse)
async def update_task_fragment(
    request: Request,
    id: str,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    status: Annotated[TaskStatus, Form()],
):
    try:
        _ = await get_task_by_id(id)
    except HTTPException as e:
        if e.status_code == 404:
            updated_task = await create_task(
                title=title,
                description=description,
                status=status,
                id=id,
            )
        else:
            raise e
    updated_task = await update_task(id, title, description, status)

    return templates.TemplateResponse(
        "components/new_task.html",
        {"request": request, "task": updated_task, "status": updated_task.status.value},
    )


@router.delete("/htmx/task/{id}", response_class=HTMLResponse)
async def delete_task_fragment(request: Request, id: str):
    await delete_task(id)
    return ""


@router.delete("/htmx/task/cancel/{id}", response_class=HTMLResponse)
async def delete_task_fragment(request: Request, id: str):
    try:
        task = await get_task_by_id(id)
    except HTTPException as e:
        if e.status_code == 404:
            return ""
        raise e

    return templates.TemplateResponse(
        "components/new_task.html",
        {"request": request, "task": task, "status": task.status.value},
    )
