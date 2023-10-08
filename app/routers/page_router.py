from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.settings import templates

import asyncio

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/update_todo", response_class=HTMLResponse)
async def home_page(request: Request):
    await asyncio.sleep(2)
    return """
<h2>tset</h2>
"""
    return templates.TemplateResponse("index.html", {"request": request})
