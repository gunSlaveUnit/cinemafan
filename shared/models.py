from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Entity(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
