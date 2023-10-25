from typing import List
from fastapi import HTTPException, status
from app.core.settings import settings
import httpx
from loguru import logger
from app.schemas.tasks import Task, TaskStatus


async def get_tasks() -> List[Task]:
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
    return tasks


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
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{settings.pb_host}/api/collections/task/records/{id}")
    if r.status_code == 404:
        return None
    elif r.status_code != 204:
        logger.error(str(r.text))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r.text)
        )


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
    return task
