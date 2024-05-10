from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Movie
from movies.schemas import MovieCreateSchema
from root.db import session

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def items(db: AsyncSession = Depends(session)):
    data = [_ async for _ in Movie.every(db)]

    return {
        "data": data,
        "length": len(data),
    }


@router.get("/{item_id}")
async def item(item_id: int, db: AsyncSession = Depends(session)):
    return await Movie.by_id(item_id, db)


@router.post("")
async def create(data: MovieCreateSchema, db: AsyncSession = Depends(session)):
    return await Movie.create(data.model_dump(), db)
