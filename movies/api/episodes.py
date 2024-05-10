from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Quality, Episode
from movies.schemas import EpisodeCreateSchema
from root.db import session

router = APIRouter(prefix="/episodes", tags=["Episodes"])


@router.get("")
async def items(db: AsyncSession = Depends(session)):
    data = [_ async for _ in Episode.every(db)]

    return {
        "data": data,
        "length": len(data),
    }


@router.get("/{item_id}")
async def item(item_id: int, db: AsyncSession = Depends(session)):
    return await Episode.by_id(item_id, db)


@router.post("")
async def create(data: EpisodeCreateSchema, db: AsyncSession = Depends(session)):
    return await Episode.create(data.model_dump(), db)
