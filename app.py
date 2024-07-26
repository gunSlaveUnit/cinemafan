import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles 

from infrastructure.settings import MEDIA_DIR, STATIC_DIR
from infrastructure.db import init
from movies.routes import router as movies_router
from videos.routes import router as videos_router
from root.routes import router as root_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    os.makedirs(MEDIA_DIR, exist_ok=True)

    await init()

    yield


app = FastAPI(
    title="cinemafan",
    version="0.19.0",
    lifespan=lifespan,
)

app.mount(
    "/media", 
    StaticFiles(directory=MEDIA_DIR), 
    name="media",
)
app.mount(
    "/static", 
    StaticFiles(directory=STATIC_DIR), 
    name="static",
)

app.include_router(movies_router)
app.include_router(root_router)
app.include_router(videos_router)
