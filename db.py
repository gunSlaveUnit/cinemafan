"""Provides functions for initializing the database and
obtaining asynchronous sessions.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.models import Base
from settings import DB_URL

engine: AsyncEngine = create_async_engine(DB_URL)
session_maker: async_sessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def init() -> None:
    """Creates database tables if they aren't 

    Returns:
        None
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Provides database session.

    Returns:
        AsyncGenerator[AsyncSession]: database session.
    """

    async with session_maker() as s:
        try:
            yield s
        finally:
            await s.close()
