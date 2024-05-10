from fastapi import APIRouter

from movies.api.episodes import router as episodes_api_router
from movies.api.movies import router as movies_api_router
from movies.api.qualities import router as qualities_api_router
from movies.api.records import router as records_api_router
from movies.templates.episodes import router as episodes_templates_router
from movies.templates.movies import router as movies_templates_router

api_router = APIRouter(prefix="/api", tags=["API"])
api_router.include_router(episodes_api_router)
api_router.include_router(movies_api_router)
api_router.include_router(qualities_api_router)
api_router.include_router(records_api_router)

templates_router = APIRouter(prefix="", tags=["Templates"])
templates_router.include_router(episodes_templates_router)
templates_router.include_router(movies_templates_router)

router = APIRouter()
router.include_router(api_router)
router.include_router(templates_router)
