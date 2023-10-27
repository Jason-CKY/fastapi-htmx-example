from pydantic import BaseModel
from enum import Enum
from typing import List


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    PROGRESS = "progress"
    DONE = "done"


class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus


class TaskSort(BaseModel):
    id: str
    status: TaskStatus
    sorting_order: List[str]
