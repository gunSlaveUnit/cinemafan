from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from movies.routes import router as movies_router
from root.db import init
from root.routes import router as root_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await init()

    yield


app = FastAPI(
    title="cinemafan",
    version="0.1.1",
    lifespan=lifespan,
)

app.include_router(root_router)
app.include_router(movies_router)
