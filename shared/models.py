from typing import AsyncIterator
import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Entity(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True, 
    )

    @classmethod
    async def every(cls, session: AsyncSession) -> AsyncIterator:
        scalars = await session.stream_scalars(select(cls))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_id(
            cls,
            item_id: uuid.UUID,
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

    async def update(
            self,
            data: dict,
            session: AsyncSession,
    ):
        for attribute, value in data.items():
            setattr(self, attribute, value)

        await session.commit()
        await session.refresh(self)
