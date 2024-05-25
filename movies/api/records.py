from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.models import Record
from movies.schemas import RecordCreateSchema
from infrastructure.db import get_db

router = APIRouter(prefix="/records", tags=["Records"])


@router.get("")
async def items(db: AsyncSession = Depends(get_db)):
    data = [_ async for _ in Record.every(db)]

    return {
        "data": data,
        "length": len(data),
    }


@router.get("/{item_id}")
async def item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await Record.by_id(item_id, db)


@router.post("")
async def create(data: RecordCreateSchema, db: AsyncSession = Depends(get_db)):
    return await Record.create(data.model_dump(), db)
