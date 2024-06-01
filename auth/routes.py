from fastapi import APIRouter

from auth.api import router as auth_router
from auth.templates import router as auth_templates_router

api_router = APIRouter(prefix="/api", tags=["API"])
api_router.include_router(auth_router)

templates_router = APIRouter(prefix="", tags=["Templates"])
templates_router.include_router(auth_templates_router)

router = APIRouter()
router.include_router(api_router)
router.include_router(templates_router)
