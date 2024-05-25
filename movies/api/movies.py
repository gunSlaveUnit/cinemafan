from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Movie
from movies.schemas import MovieCreateSchema
from infrastructure.db import get_db

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def items(db: AsyncSession = Depends(get_db)):
    data = [_ async for _ in Movie.every(db)]

    return {
        "data": data,
        "length": len(data),
    }


@router.get("/{item_id}")
async def item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await Movie.by_id(item_id, db)


@router.post("")
async def create(data: MovieCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Movie.create(data.model_dump(), db)
