"""Contains paths, constants, etc.
All environment variables are loaded from the .env file here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

DEBUG: bool = os.getenv("DEBUG") == "True"
"""bool: Whether to run the server in debug mode.

Determines whether static and media files should be mounted.
Typically, if debugging is disabled, they will be managed by NGINX.
"""

BASE_DIR: Path = Path(__file__).resolve().parent
"""Path: Base directory of the project."""

MEDIA_DIR: Path = BASE_DIR / "media"
"""Path: Directory for media files like images and videos."""

STATIC_DIR: Path = BASE_DIR / "static"
"""Path: Directory for static files like CSS and JS."""

TEMPLATES_DIR: Path = BASE_DIR / "templates"
"""Path: Directory for templates - HTML with Jinja."""

APP_NAME: str = "cinemafan"
"""str: Name of the application."""

VERSION: str = "0.35.0"
"""str: Version of the application in semantic format (major.minor.patch)."""

HOST: str = os.getenv("HOST")
"""str: Hostname of the server."""

PORT: int = int(os.getenv("PORT"))
"""int: Port number of the server."""

RELOAD: bool = os.getenv("RELOAD") == "True"
"""bool: Whether to run the server in reload mode.

If enabled, the server will be restarted on file changes.
"""

WORKERS: int = 1 if RELOAD else os.cpu_count() + 1
"""int: Number of workers to use in FastAPI app.

If `RELOAD` is enabled, this value is ignored and
set to 1 because FastAPI does not support reloading in multi-worker mode.
"""

DB_URL: str = os.getenv("DB_URL")
"""str: Database connection string."""

SECRET_KEY: str = os.getenv("SECRET_KEY")
"""str: Secret key for JWT tokens."""

ALGORITHM: str = os.getenv("ALGORITHM")
"""str: Algorithm for JWT tokens."""

base_context: dict = {
    "app_name": APP_NAME,
    "current_year": None,
    "user": None,
    "version": VERSION,
}
"""dict: Base context for templates.

Contains data that should appear on all pages of the application.
The display of such data is prescribed in templates/base.html.
"""

templates: Jinja2Templates = Jinja2Templates(directory=TEMPLATES_DIR)
"""Jinja2Templates: Jinja2 templates for the application."""
