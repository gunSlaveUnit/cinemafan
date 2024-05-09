from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request

from movies.routes import router as movies_router
from root.db import init
from root.templates import templates


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init()

    yield


app = FastAPI(
    title="cinemafan",
    lifespan=lifespan,
)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


app.include_router(movies_router)
