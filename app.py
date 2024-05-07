from fastapi import FastAPI, Request

from movies.routes import router as movies_router
from root.templates import templates

app = FastAPI(
    title="cinemafan",
)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

app.include_router(movies_router)
