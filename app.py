from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles 

from auth.routes import router as auth_router
from infrastructure.settings import MEDIA_DIR
from infrastructure.db import init
from movies.routes import router as movies_router
from player.routes import router as player_router
from root.routes import router as root_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init()

    yield


app = FastAPI(
    title="cinemafan",
    version="0.15.0",
    lifespan=lifespan,
)

app.mount(
    "/media", 
    StaticFiles(directory=MEDIA_DIR), 
    name="media",
)

app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(player_router)
app.include_router(root_router)
