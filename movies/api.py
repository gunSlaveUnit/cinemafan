from fastapi import APIRouter

from movies.endpoints import episodes, movies, qualities, records
from movies.templates import router as templates_router

router = APIRouter()

api_router = APIRouter(prefix="/api", tags=["API"])

api_router.include_router(episodes.router)
api_router.include_router(movies.router)
api_router.include_router(qualities.router)
api_router.include_router(records.router)

router.include_router(api_router)
router.include_router(templates_router)
