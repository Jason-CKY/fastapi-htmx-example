import os
import sys
from loguru import logger
from pathlib import Path
from pydantic_settings import BaseSettings

# from fastapi.templating import Jinja2Templates
from jinja2_fragments.fastapi import Jinja2Blocks


class Settings(BaseSettings):
    app_name: str = "FastAPI htmx server"
    app_description: str = "htmx web server written in FastAPI"
    app_version: str = os.getenv("APP_VERSION", "0.0.1")
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")

    swagger_js_url: str = os.getenv(
        "SWAGGER_JS_URL",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    )
    swagger_css_url: str = os.getenv(
        "SWAGGER_CSS_URL",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

    pb_host: str
    pb_admin_username: str
    pb_admin_password: str


settings = Settings()
templates = Jinja2Blocks(directory=Path(__file__).parent.parent / "templates")

logger.remove()
logger.add(sys.stdout, level=settings.log_level)
