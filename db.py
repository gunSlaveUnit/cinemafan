"""Provides functions for initializing the database and
obtaining asynchronous sessions.
"""

from typing import AsyncGenerator

import psycopg
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
    """Creates database tables if they do not exist 

    Returns:
        None
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides database session.

    Returns:
        AsyncGenerator[AsyncSession]: database session.
    """

    async with session_maker() as s:
        try:
            yield s
        finally:
            await s.close()


async def get_cursor():
    async with await psycopg.AsyncConnection.connect("postgresql://postgres:postgres@localhost:5432/cinemafan") as connection:
        async with connection.cursor() as cursor:
            yield cursor
