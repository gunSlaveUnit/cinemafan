from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from movies.models import Age
from movies.schemas import AgeCreateSchema
from root.models import Base
from infrastructure.settings import DB_CONFIG


def build_url(data: dict) -> str:
    """
    Builds url for database connection.

    Args:
        data: database connection data.

    Returns:
        str: url for database connection.
    """

    engine = data.get("engine")
    name = data.get("name")
    user = data.get("user")
    password = data.get("password")
    host = data.get("host")
    port = data.get("port")

    auth: str = (
        f"{user}:{password}"
        if user is not None and password is not None
        else user if user is not None else None
    )
    location: str = (
        f"{host}:{port}"
        if host is not None and port is not None
        else host if host is not None else None
    )
    credentials: str = (
        f"{auth}@{location}"
        if auth is not None and location is not None
        else location if location is not None else None
    )

    return (
        f"{engine}://{credentials}/{name}"
        if credentials is not None
        else f"{engine}:///{name}"
    )


DB_URL = build_url(DB_CONFIG)

engine: AsyncEngine = create_async_engine(DB_URL)
session_maker: async_sessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def init() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as s:
        try:
            ages = [_ async for _ in Age.every(s)]
            if not ages:
                await Age.create(AgeCreateSchema(title="G", description="All ages").model_dump(), s)
                await Age.create(AgeCreateSchema(title="PG", description="Parental guidance").model_dump(), s)
                await Age.create(
                    AgeCreateSchema(
                        title="PG-13",
                        description="Parents strongly cautioned",
                    ).model_dump(),
                    s,
                )
                await Age.create(AgeCreateSchema(title="R", description="Restricted").model_dump(), s)
                await Age.create(AgeCreateSchema(title="NC-17", description="Adults only").model_dump(), s)
        finally:
            await s.close()


async def session() -> AsyncGenerator[AsyncSession, None]:
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
