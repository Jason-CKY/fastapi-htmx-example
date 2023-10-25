from pydantic import BaseModel
from enum import Enum


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    PROGRESS = "progress"
    DONE = "done"


class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus
