from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Movie
from movies.schemas import MovieCreateSchema
from root.db import session
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


@api_router.post("")
async def create(
        data: MovieCreateSchema,
        db: AsyncSession = Depends(session),
):
    item = Movie(**data.model_dump())

    db.add(item)
    await db.commit()
    await db.flush()

    return item


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
