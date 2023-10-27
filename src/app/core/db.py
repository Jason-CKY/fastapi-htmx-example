from typing import List, Tuple, Dict
from fastapi import HTTPException, status
from app.core.settings import settings
import httpx
import asyncio
from loguru import logger
from app.schemas.tasks import Task, TaskStatus, TaskSort


async def get_tasks() -> Tuple[List[Task], Dict[str, List[str]]]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.pb_host}/api/collections/task/records",
        )
    if r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )
    response = r.json()
    tasks = []
    for item in response["items"]:
        task = Task(
            id=item["id"],
            title=item["title"],
            description=item["description"],
            status=item["status"],
        )
        tasks.append(task)

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.pb_host}/api/collections/task_sorting/records",
        )
    if r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )

    response = r.json()
    order = {TaskStatus.BACKLOG: [], TaskStatus.PROGRESS: [], TaskStatus.DONE: []}
    for item in response["items"]:
        if item["status"] == TaskStatus.BACKLOG:
            order[TaskStatus.BACKLOG] = item["sorting_order"]
        elif item["status"] == TaskStatus.PROGRESS:
            order[TaskStatus.PROGRESS] = item["sorting_order"]
        elif item["status"] == TaskStatus.DONE:
            order[TaskStatus.DONE] = item["sorting_order"]

    return tasks, order


async def get_task_by_id(id: str) -> Task:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.pb_host}/api/collections/task/records/{id}",
        )
    if r.status_code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )

    response = r.json()
    task = Task(
        id=response["id"],
        title=response["title"],
        description=response["description"],
        status=response["status"],
    )
    return task


async def delete_task(id: str) -> None:
    task = await get_task_by_id(id)
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{settings.pb_host}/api/collections/task/records/{id}")
    if r.status_code == 404:
        return None
    elif r.status_code != 204:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )

    task_order = await get_task_order(task.status)
    task_order.sorting_order = [
        order for order in task_order.sorting_order if order != task.id
    ]
    await update_task_order(task_order.id, task_order.sorting_order)


async def update_task(
    id: str, title: str, description: str, status: TaskStatus
) -> Task:
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{settings.pb_host}/api/collections/task/records/{id}",
            json={
                "title": title,
                "description": description,
                "status": status,
            },
        )
    if r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )
    response = r.json()
    task = Task(
        id=response["id"],
        title=response["title"],
        description=response["description"],
        status=response["status"],
    )
    return task


async def create_task(
    title: str, description: str, status: TaskStatus, id: str = None
) -> Task:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{settings.pb_host}/api/collections/task/records",
            json={
                "id": id,
                "title": title,
                "description": description,
                "status": status,
            },
        )
    if r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )
    response = r.json()
    task = Task(
        id=response["id"],
        title=response["title"],
        description=response["description"],
        status=response["status"],
    )

    task_order = await get_task_order(task.status)
    task_order.sorting_order = [task.id] + task_order.sorting_order
    await update_task_order(task_order.id, task_order.sorting_order)
    return task


async def get_task_order(status: TaskStatus) -> TaskSort:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.pb_host}/api/collections/task_sorting/records?filter=(status='{status.value}')",
        )
    if r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )
    response = r.json()
    return TaskSort(
        id=response["items"][0]["id"],
        status=response["items"][0]["status"],
        sorting_order=response["items"][0]["sorting_order"]
        if response["items"][0]["sorting_order"] is not None
        else [],
    )


async def update_task_order(id: str, sorting_order: List[str]) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{settings.pb_host}/api/collections/task_sorting/records/{id}",
            json={"sorting_order": sorting_order},
        )
    if r.status_code != 200:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )


async def update_tasks_order(
    backlog_tasks: List[Task], progress_tasks: List[Task], done_tasks: List[Task]
) -> None:
    backlog_sort, progress_sort, done_sort = await asyncio.gather(
        get_task_order(TaskStatus.BACKLOG),
        get_task_order(TaskStatus.PROGRESS),
        get_task_order(TaskStatus.DONE),
    )
    await asyncio.gather(
        update_task_order(
            id=backlog_sort.id, sorting_order=[task.id for task in backlog_tasks]
        ),
        update_task_order(
            id=progress_sort.id, sorting_order=[task.id for task in progress_tasks]
        ),
        update_task_order(
            id=done_sort.id, sorting_order=[task.id for task in done_tasks]
        ),
    )
