import os
from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
TEMPLATES_DIR = BASE_DIR / "templates"

os.makedirs(MEDIA_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)
