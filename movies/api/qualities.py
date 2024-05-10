from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Quality
from movies.schemas import QualityCreateSchema
from infrastructure.db import session

router = APIRouter(prefix="/qualities", tags=["Qualities"])


@router.get("")
async def items(db: AsyncSession = Depends(session)):
    data = [_ async for _ in Quality.every(db)]

    return {
        "data": data,
        "length": len(data),
    }


@router.get("/{item_id}")
async def item(item_id: int, db: AsyncSession = Depends(session)):
    return await Quality.by_id(item_id, db)


@router.post("")
async def create(data: QualityCreateSchema, db: AsyncSession = Depends(session)):
    return await Quality.create(data.model_dump(), db)
