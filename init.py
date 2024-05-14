import asyncio
import datetime

from movies.models import Age, Movie, Episode, Quality, Record, Category, Season
from infrastructure.db import session_maker
from movies.schemas import AgeCreateSchema, MovieCreateSchema, EpisodeCreateSchema, QualityCreateSchema, \
    RecordCreateSchema, CategoryCreateSchema, SeasonCreateSchema


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


async def create_categories():
    async with session_maker() as s:
        try:
            await Category.create(CategoryCreateSchema(title="Full-length").model_dump(), s)
            await Category.create(CategoryCreateSchema(title="Short-length").model_dump(), s)
            await Category.create(CategoryCreateSchema(title="Series").model_dump(), s)
        finally:
            await s.close()


async def create_qualities():
    async with session_maker() as s:
        try:
            await Quality.create(QualityCreateSchema(resolution=360).model_dump(), s)
            await Quality.create(QualityCreateSchema(resolution=480).model_dump(), s)
            await Quality.create(QualityCreateSchema(resolution=720).model_dump(), s)
            await Quality.create(QualityCreateSchema(resolution=1080).model_dump(), s)
            await Quality.create(QualityCreateSchema(resolution=2160).model_dump(), s)
            await Quality.create(QualityCreateSchema(resolution=4320).model_dump(), s)
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
                    category_id=3,
                ).model_dump(),
                s,
            )
        finally:
            await s.close()


async def create_seasons():
    async with session_maker() as s:
        try:
            await Season.create(
                SeasonCreateSchema(
                    number=1,
                    movie_id=1,
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
                    season_id=1,
                    title="The Fate of Particular Adventurers",
                    release_date=datetime.datetime(2018, 10, 7),
                ).model_dump(),
                s,
            )
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=2,
                    season_id=1,
                    title="Goblin Slayer",
                    release_date=datetime.datetime(2018, 10, 14),
                ).model_dump(),
                s,
            )
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=3,
                    season_id=1,
                    title="Unexpected Visitors",
                    release_date=datetime.datetime(2018, 10, 21),
                ).model_dump(),
                s,
            )
            await Episode.create(
                EpisodeCreateSchema(
                    movie_id=1,
                    number=4,
                    season_id=1,
                    title="The Strong",
                    release_date=datetime.datetime(2018, 10, 28),
                ).model_dump(),
                s,
            )
        finally:
            await s.close()


async def create_records():
    async with session_maker() as s:
        try:
            await Record.create(
                RecordCreateSchema(
                    episode_id=1,
                    quality_id=1,
                    filename="73a48dd8-7250-4c61-9539-ea256567a70c.mp4",
                ).model_dump(),
                s,
            )
            await Record.create(
                RecordCreateSchema(
                    episode_id=1,
                    quality_id=2,
                    filename="6e7182ee-ae60-4ba3-84e8-f509003b6266.mp4",
                ).model_dump(),
                s,
            )
            await Record.create(
                RecordCreateSchema(
                    episode_id=1,
                    quality_id=3,
                    filename="2816587b-1bac-4c24-bb6d-8a59efc372fd.mp4",
                ).model_dump(),
                s,
            )
            await Record.create(
                RecordCreateSchema(
                    episode_id=1,
                    quality_id=4,
                    filename="35504036-35d9-4024-a0fe-eda11cf684ab.mp4",
                ).model_dump(),
                s,
            )
        finally:
            await s.close()


async def init():
    await create_ages()
    await create_qualities()
    await create_categories()
    await create_seasons()
    await create_movies()
    await create_episodes()
    await create_records()


asyncio.run(init())
