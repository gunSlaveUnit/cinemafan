from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Movie
from movies.schemas import MovieCreateSchema
from root.db import session

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def items(db: AsyncSession = Depends(session)):
    scalars = await db.stream_scalars(select(Movie))

    data = [_ async for _ in scalars]

    return {
        "data": data,
        "length": len(data),
    }


@router.post("")
async def create(
        data: MovieCreateSchema,
        db: AsyncSession = Depends(session),
):
    e = Movie(**data.model_dump())

    db.add(e)
    await db.commit()
    await db.flush()

    return e


@router.get("/{item_id}")
async def item(
        item_id: int,
        db: AsyncSession = Depends(session),
):
    e = await db.scalar(select(Movie).where(Movie.id == item_id))
    return e
