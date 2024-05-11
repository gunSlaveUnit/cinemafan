import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
TEMPLATES_DIR = BASE_DIR / "templates"

os.makedirs(MEDIA_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)

DB_CONFIG = {
    "engine": os.getenv("DB_ENGINE"),
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
