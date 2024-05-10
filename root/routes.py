from fastapi import APIRouter

from root.templates.index import router as index_router

templates_router = APIRouter(prefix="", tags=["Templates"])
templates_router.include_router(index_router)

router = APIRouter()
router.include_router(templates_router)
