from fastapi import APIRouter, Request

from root.templates import templates

api_router = APIRouter(prefix="/api/movies", tags=["Movies", "API"])
templates_router = APIRouter(prefix="/movies", tags=["Movies", "Templates"])


@templates_router.get("")
async def items(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
    )
