from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

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

app.include_router(index_router)
app.include_router(movies_api_router)
app.include_router(movies_templates_router)
