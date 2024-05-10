from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, APIRouter

from movies.api import router as movies_api_router
from movies.templates import router as movies_templates_router
from root.db import init
from root.templates import router as index_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await init()

    yield


app = FastAPI(
    title="cinemafan",
    version="0.1.1",
    lifespan=lifespan,
)

api_router = APIRouter(prefix="/api", tags=["API"])
api_router.include_router(movies_api_router)

templates_router = APIRouter(prefix="", tags=["Templates"])
templates_router.include_router(index_router)
templates_router.include_router(movies_templates_router)

app.include_router(api_router)
app.include_router(templates_router)
