from fastapi import FastAPI, Request

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
