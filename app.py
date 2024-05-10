from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, APIRouter

from movies.api import router as movies_router
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
app.include_router(movies_router)
