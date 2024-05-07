from fastapi.templating import Jinja2Templates

from root.settings import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)
