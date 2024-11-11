from sqlalchemy import select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class User(Entity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

    @classmethod
    async def by_name(
            cls,
            name: str,
            session: AsyncSession,
    ):
        return await session.scalar(select(cls).where(cls.name == name))
