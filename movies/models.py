import datetime

from sqlalchemy import String, ForeignKey, select, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class Person(Entity):
    __tablename__ = "persons"

    name: Mapped[str] = mapped_column(String(255))


class Age(Entity):
    __tablename__ = "ages"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)


class Category(Entity):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(255))


class Movie(Entity):
    __tablename__ = "movies"

    original_title: Mapped[str] = mapped_column(String(255))
    translated_title: Mapped[str] = mapped_column(String(255))
    poster: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    age_id: Mapped[int] = mapped_column(ForeignKey("ages.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))


class Genre(Entity):
    __tablename__ = "genres"

    title: Mapped[str] = mapped_column(String(255))


class MovieGenre(Entity):
    __tablename__ = "movies_genres"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Tag(Entity):
    __tablename__ = "tags"

    title: Mapped[str] = mapped_column(String(255))


class Tagging(Entity):
    __tablename__ = "taggings"

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


class Season(Entity):
    __tablename__ = "seasons"

    number: Mapped[int]
    title: Mapped[str] = mapped_column(String(255), nullable=True)
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


class Quality(Entity):
    __tablename__ = "qualities"

    resolution: Mapped[int]


class Record(Entity):
    __tablename__ = "records"

    episode_id: Mapped[int] = mapped_column(ForeignKey("episodes.id"))
    quality_id: Mapped[int] = mapped_column(ForeignKey("qualities.id"))
    filename: Mapped[str] = mapped_column(String(255))

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

    title: Mapped[str] = mapped_column(String(255))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    filename: Mapped[str] = mapped_column(String(255))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar
