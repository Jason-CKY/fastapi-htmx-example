from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.settings import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    return "<h1>Hello World</h1>"
