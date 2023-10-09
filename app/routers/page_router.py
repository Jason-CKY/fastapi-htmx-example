from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.core.settings import templates
from app.core.db import get_todos, create_todo
import asyncio

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "todos": get_todos()
        }
    )


@router.get("/htmx/todo", response_class=HTMLResponse)
async def todo_fragment(request: Request):
    await asyncio.sleep(1)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "todos": get_todos()
        },
        block_name="content"
    )


@router.post("/htmx/todo", response_class=HTMLResponse)
async def create_todo_fragment(request: Request, todo: Annotated[str, Form()]):
    create_todo(todo)
    await asyncio.sleep(1)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "todos": get_todos()
        },
        block_name="content"
    )
