import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

VERSION="0.28.0"

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
RELOAD = os.getenv("RELOAD") == "True"
WORKERS = 1 if RELOAD else os.cpu_count() + 1

DB_URL = os.getenv("DB_URL")

templates = Jinja2Templates(directory=TEMPLATES_DIR)
