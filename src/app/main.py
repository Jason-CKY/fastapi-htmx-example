from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import httpx

from app.core.settings import settings, templates
from app.routers import page_router
from loguru import logger


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=None,  # Disable so that our override (below) will work
    redoc_url=None,  # Disable
)


@app.get("/docs", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_js_url=settings.swagger_js_url,
        swagger_css_url=settings.swagger_css_url,
        swagger_favicon_url="/static/favicon.png",
    )


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/health", include_in_schema=False)
def healthcheck():
    return {"message": "Healthy!"}


app.include_router(page_router.router, tags=["Pages"], prefix="/htmx")

# serve all files in /static/*
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"))
