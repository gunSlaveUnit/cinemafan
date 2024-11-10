import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles 

from settings import DEBUG, MEDIA_DIR, STATIC_DIR, VERSION
from db import init

from auth.routes import router as auth_router
from movies.routes import router as movies_router
from videos.routes import router as videos_router
from root.routes import router as root_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    os.makedirs(MEDIA_DIR, exist_ok=True)

    await init()

    yield


app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan,
    title="cinemafan",
    version=VERSION,
)

if DEBUG:
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

app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(root_router)
app.include_router(videos_router)
