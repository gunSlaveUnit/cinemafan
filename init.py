import asyncio

from movies.models import Age
from infrastructure.db import session_maker
from movies.schemas import AgeCreateSchema


async def init():
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


asyncio.run(init())
