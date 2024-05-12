import asyncio
import datetime

from movies.models import Age, Movie, Episode
from infrastructure.db import session_maker
from movies.schemas import AgeCreateSchema, MovieCreateSchema, EpisodeCreateSchema


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


async def create_episodes():
    async with session_maker() as s:
        try:
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=1,
                    season=1,
                    title="The Fate of Particular Adventurers",
                    release_date=datetime.datetime(2018, 10, 7),
                ).model_dump(),
                s,
            )
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=2,
                    season=1,
                    title="Goblin Slayer",
                    release_date=datetime.datetime(2018, 10, 14),
                ).model_dump(),
                s,
            )
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=3,
                    season=1,
                    title="Unexpected Visitors",
                    release_date=datetime.datetime(2018, 10, 21),
                ).model_dump(),
                s,
            )
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=4,
                    season=1,
                    title="The Strong",
                    release_date=datetime.datetime(2018, 10, 28),
                ).model_dump(),
                s,
            )
        finally:
            await s.close()


async def init():
    await create_ages()
    await create_movies()


asyncio.run(init())
