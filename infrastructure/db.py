import os


from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.models import Base



DB_URL = os.getenv("DB_URL")

engine: AsyncEngine = create_async_engine(DB_URL)
session_maker: async_sessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with session_maker() as s:
        try:
            yield s
        finally:
            await s.close()
