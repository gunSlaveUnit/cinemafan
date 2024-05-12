import asyncio

from movies.models import Age, Movie
from infrastructure.db import session_maker
from movies.schemas import AgeCreateSchema, MovieCreateSchema


async def create_ages():
    async with session_maker() as s:
        try:
            await Age.create(AgeCreateSchema(title="G", description="All ages").model_dump(), s)
            await Age.create(AgeCreateSchema(title="PG", description="Parental guidance").model_dump(), s)
            await Age.create(AgeCreateSchema(title="PG-13", description="Parents strongly cautioned").model_dump(), s)
            await Age.create(AgeCreateSchema(title="R", description="Restricted").model_dump(), s)
            await Age.create(AgeCreateSchema(title="NC-17", description="Adults only").model_dump(), s)
        finally:
            await s.close()


async def create_movies():
    async with session_maker() as s:
        try:
            await Movie.create(
                MovieCreateSchema(
                    title="Goblin Slayer",
                    poster="cfd37e0a-e162-4a66-9af6-f62bced5082b.jpg",
                    description="Any group of adventurers must have a healer; most often this role falls to priests. "
                                "A young Priestess joins such a team and during her first outing she encounters a "
                                "bunch of evil goblins who attack her comrades, leaving the girl in shock. The "
                                "priestess's first adventure could have been her last, if not for a mysterious "
                                "stranger from the Dungeon - a knight called Goblin Slayer. And, it must be said, "
                                "he lives up to his nickname - the offspring die from his sword, like flies. The girl "
                                "decides to keep an eye on him and give him the opportunity to destroy the green "
                                "scourge. To do this, she will have to study stronger and more complex magic, "
                                "as well as learn a lot of new things about her enemies. Only some secrets are better "
                                "like yours...",
                    age_id=5,
                ).model_dump(),
                s,
            )
        finally:
            await s.close()


async def init():
    await create_ages()
    await create_movies()


asyncio.run(init())
