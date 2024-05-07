from fastapi import APIRouter, Request

from root.templates import templates

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def items(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
    )
