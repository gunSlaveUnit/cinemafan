from typing import AsyncIterator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Entity(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

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
