import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

DEBUG = os.getenv("DEBUG") == "True"

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

APP_NAME = "cinemafan"
VERSION="0.32.0"

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
RELOAD = os.getenv("RELOAD") == "True"
WORKERS = 1 if RELOAD else os.cpu_count() + 1

DB_URL = os.getenv("DB_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

base_context = {
    "app_name": APP_NAME,
    "current_year": None,
    "user": None,
    "version": VERSION,
}
templates = Jinja2Templates(directory=TEMPLATES_DIR)
