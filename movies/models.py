import datetime

from sqlalchemy import String, ForeignKey, select, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class Activity(Entity):
    __tablename__ = "activities"

    title: Mapped[str] = mapped_column(String(255))


class Age(Entity):
    __tablename__ = "ages"

    description: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(String(255))


class Category(Entity):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(255))


class Episode(Entity):
    __tablename__ = "episodes"

    number: Mapped[int]
    parent_id: Mapped[int] = mapped_column(ForeignKey("episodes.id"), nullable=True)
    release_date: Mapped[datetime.datetime]
    season_id: Mapped[int]
    title: Mapped[str] = mapped_column(String(255))

    @classmethod
    async def by_season_id(
            cls,
            season_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.season_id == season_id))
        async for scalar in scalars:
            yield scalar


class Genre(Entity):
    __tablename__ = "genres"

    title: Mapped[str] = mapped_column(String(255))


class Movie(Entity):
    __tablename__ = "movies"

    age_id: Mapped[int] = mapped_column(ForeignKey("ages.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    description: Mapped[str] = mapped_column(Text)
    original_title: Mapped[str] = mapped_column(String(255))
    poster: Mapped[str] = mapped_column(String(255))
    translated_title: Mapped[str] = mapped_column(String(255))


class MovieGenre(Entity):
    __tablename__ = "movies_genres"

    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class MoviePerson(Entity):
    __tablename__ = "movies_persons"

    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class MovieStudio(Entity):
    __tablename__ = "movies_studios"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    studio_id: Mapped[int] = mapped_column(ForeignKey("studios.id"))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class MovieTag(Entity):
    __tablename__ = "movies_tags"

    accuracy: Mapped[int]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Person(Entity):
    __tablename__ = "persons"

    name: Mapped[str] = mapped_column(String(255))


class Quality(Entity):
    __tablename__ = "qualities"

    resolution: Mapped[int]


class Record(Entity):
    __tablename__ = "records"

    episode_id: Mapped[int] = mapped_column(ForeignKey("episodes.id"))
    filename: Mapped[str] = mapped_column(String(255))
    quality_id: Mapped[int] = mapped_column(ForeignKey("qualities.id"))

    @classmethod
    async def by_episode_id(
            cls,
            episode_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.episode_id == episode_id))
        async for scalar in scalars:
            yield scalar


class Screenshot(Entity):
    __tablename__ = "screenshots"

    filename: Mapped[str] = mapped_column(String(255))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    title: Mapped[str] = mapped_column(String(255))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Season(Entity):
    __tablename__ = "seasons"

    number: Mapped[int]
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=True)

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Studio(Entity):
    __tablename__ = "studios"

    title: Mapped[str] = mapped_column(String(255))


class Tag(Entity):
    __tablename__ = "tags"

    title: Mapped[str] = mapped_column(String(255))
