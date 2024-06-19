import os

from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from root.models import Base

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine: AsyncEngine = create_async_engine(DB_URL)
session_maker: async_sessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def init() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session.

    Returns:
        AsyncGenerator[AsyncSession, None]: database session.
    """

    async with session_maker() as s:
        try:
            yield s
        finally:
            await s.close()
