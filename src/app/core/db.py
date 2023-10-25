from typing import List
from fastapi import HTTPException, status
from app.core.settings import settings
import httpx

from app.schemas.tasks import Task, TaskStatus


async def get_tasks() -> List[Task]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{settings.pb_host}/api/collections/task/records",
        )
    if r.status_code != 200:
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


async def delete_task(id: str) -> None:
    pass


async def create_task(
    title: str, description: str, status: TaskStatus, id: str = None
) -> Task:
    task = Task(id=id, title=title, description=description, status=status)
    return task
