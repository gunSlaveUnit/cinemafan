import datetime
from typing import AsyncIterator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from root.models import Base


class Entity(Base):
    """
    Used as base class for all models
    with useful base fields
    like id, created_at, updated_at etc.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=None, onupdate=func.now(), nullable=True)

    @classmethod
    async def every(cls, session: AsyncSession) -> AsyncIterator:
        scalars = await session.stream_scalars(select(cls))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_id(
            cls,
            item_id: int,
            session: AsyncSession,
    ):
        return await session.scalar(select(cls).where(cls.id == item_id))

    @classmethod
    async def create(
            cls,
            data: dict,
            session: AsyncSession,
    ):
        item = cls(**data)

        session.add(item)
        await session.commit()
        await session.flush()

        return item
