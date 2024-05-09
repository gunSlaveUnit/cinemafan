from fastapi import APIRouter, Request

from root.templates import templates

api_router = APIRouter(prefix="/api/movies", tags=["Movies", "API"])
templates_router = APIRouter(prefix="/movies", tags=["Movies", "Templates"])


@api_router.get("")
async def items():
    return {
        "data": [
            {
                "title": "Test movie 1",
            },
            {
                "title": "Test movie 2",
            }
        ]
    }


@templates_router.get("")
async def movies(request: Request):
    content = await items()

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "movies": content["data"],
        }
    )
