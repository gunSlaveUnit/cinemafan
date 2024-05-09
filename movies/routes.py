from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Movie
from movies.schemas import MovieCreateSchema
from root.db import session
from root.templates import templates

api_router = APIRouter(prefix="/api/movies", tags=["Movies", "API"])
templates_router = APIRouter(prefix="/movies", tags=["Movies", "Templates"])


@api_router.get("")
async def items(db: AsyncSession = Depends(session)):
    scalars = await db.stream_scalars(select(Movie))

    data = [_ async for _ in scalars]

    return {
        "data": data,
        "length": len(data),
    }


@api_router.post("")
async def create(
        data: MovieCreateSchema,
        db: AsyncSession = Depends(session),
):
    e = Movie(**data.model_dump())

    db.add(e)
    await db.commit()
    await db.flush()

    return e


@api_router.get("/{item_id}")
async def item(
        item_id: int,
        db: AsyncSession = Depends(session),
):
    e = await db.scalar(select(Movie).where(Movie.id == item_id))
    return e


@templates_router.get("")
async def movies(
        request: Request,
        db: AsyncSession = Depends(session)
):
    content = await items(db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "movies": content["data"],
        }
    )
