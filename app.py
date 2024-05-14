from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from movies.routes import router as movies_router
from infrastructure.db import init
from root.routes import router as root_router
from infrastructure.settings import MEDIA_DIR


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await init()

    yield


app = FastAPI(
    title="cinemafan",
    version="0.1.8",
    lifespan=lifespan,
)

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(root_router)
app.include_router(movies_router)
