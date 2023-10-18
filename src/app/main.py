from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import httpx

from app.core.settings import settings
from app.routers import page_router
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    # create the first admin user on pocketbase if not already created
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{settings.pb_host}/api/admins",
            json={
                "email": settings.pb_admin_username,
                "password": settings.pb_admin_password,
                "passwordConfirm": settings.pb_admin_password,
            },
        )
    if r.status_code == 401:
        logger.info("Pocketbase admin user already created")
    elif r.status_code == 200:
        logger.info("Pocketbase admin user created")
    else:
        logger.info(f"Error creating pocketbase admin user. Details: {r.text}")
    yield
    # on destroy


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=None,  # Disable so that our override (below) will work
    redoc_url=None,  # Disable
    lifespan=lifespan,
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


@app.get("/health", include_in_schema=False)
def healthcheck():
    return {"message": "Healthy!"}


app.include_router(page_router.router, tags=["Pages"])

# serve all files in /static/*
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"))
