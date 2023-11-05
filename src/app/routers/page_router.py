from typing import Annotated, List
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import (
    get_tasks,
    create_task,
    delete_task,
    get_task_by_id,
    update_task,
    update_tasks_order,
    update_task_order,
    update_tasks_status,
)
from app.schemas.tasks import TaskStatus
from loguru import logger
from uuid import uuid4

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def home_page(request: Request):
    tasks, order = await get_tasks()
    backlog, inProgress, done = [], [], []
    backlog_order = (
        order[TaskStatus.BACKLOG] if order[TaskStatus.BACKLOG] is not None else []
    )
    progress_order = (
        order[TaskStatus.PROGRESS] if order[TaskStatus.PROGRESS] is not None else []
    )
    done_order = order[TaskStatus.DONE] if order[TaskStatus.DONE] is not None else []
    if len(backlog_order) + len(progress_order) + len(done_order) != len(tasks):
        logger.critical("SOMETHING IS WRONG")
        for task in tasks:
            if task.status == "backlog":
                backlog.append(task)
            elif task.status == "progress":
                inProgress.append(task)
            else:
                done.append(task)
        await update_tasks_order(backlog, inProgress, done)

    else:
        while len(backlog_order) + len(progress_order) + len(done_order) != 0:
            if len(backlog_order) > 0:
                backlog.append(
                    [task for task in tasks if task.id == backlog_order[0]][0]
                )
                backlog_order = backlog_order[1:]
            if len(progress_order) > 0:
                inProgress.append(
                    [task for task in tasks if task.id == progress_order[0]][0]
                )
                progress_order = progress_order[1:]
            if len(done_order) > 0:
                done.append([task for task in tasks if task.id == done_order[0]][0])
                done_order = done_order[1:]

    return templates.TemplateResponse(
        "components/tasks_view.html",
        {
            "request": request,
            "backlog": backlog,
            "inProgress": inProgress,
            "done": done,
        },
    )


@router.post("/task/empty/{status}", response_class=HTMLResponse)
async def create_empty_task_fragment(request: Request, status: TaskStatus):
    return templates.TemplateResponse(
        "components/edit_task.html",
        {
            "request": request,
            "id": str(uuid4()),
            "status": status.value,
            "title": "",
            "description": "",
        },
    )


@router.post("/task/{id}", response_class=HTMLResponse)
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


@router.put("/task/{id}", response_class=HTMLResponse)
async def update_task_fragment(
    request: Request,
    id: str,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    status: Annotated[str, Form()],
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


@router.delete("/task/{id}", response_class=HTMLResponse)
async def delete_task_fragment(request: Request, id: str):
    await delete_task(id)
    return ""


@router.delete("/task/cancel/{id}", response_class=HTMLResponse)
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


@router.post("/sort/{status}", response_class=HTMLResponse)
async def update_task_sorting(
    request: Request, status: TaskStatus, task_ids: Annotated[List[str], Form()]
):
    await update_task_order(status=status, sorting_order=task_ids)
    tasks = await update_tasks_status(task_ids, status)

    return templates.TemplateResponse(
        "components/task_list.html",
        {"request": request, "tasks": tasks, "status": status.value},
    )
