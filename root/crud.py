from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from root.db import session


def crud(router, model, create_schema):
    @router.get("")
    async def items(db: AsyncSession = Depends(session)):
        data = [_ async for _ in model.every(db)]

        return {
            "data": data,
            "length": len(data),
        }

    @router.post("")
    async def create(
            data: create_schema,
            db: AsyncSession = Depends(session),
    ):
        return await model.create(data.model_dump(), db)

    @router.get("/{item_id}")
    async def item(
            item_id: int,
            db: AsyncSession = Depends(session),
    ):
        return model.by_id(item_id, db)
