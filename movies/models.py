import datetime
import uuid

from sqlalchemy import String, select, Text
from sqlalchemy.dialects.postgresql import UUID
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

    duration: Mapped[float]
    number: Mapped[int]
    parent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    release_date: Mapped[datetime.datetime]
    season_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(255))

    @classmethod
    async def by_season_id(
            cls,
            season_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.season_id == season_id))
        async for scalar in scalars:
            yield scalar


class Genre(Entity):
    __tablename__ = "genres"

    title: Mapped[str] = mapped_column(String(255))


class Moment(Entity):
    __tablename__ = "moments"

    content: Mapped[str] = mapped_column(Text)
    episode_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    time: Mapped[float]

    @classmethod
    async def by_episode_id(
            cls,
            episode_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.episode_id == episode_id))
        async for scalar in scalars:
            yield scalar


class Movie(Entity):
    __tablename__ = "movies"

    age_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    description: Mapped[str] = mapped_column(Text)
    original_title: Mapped[str] = mapped_column(String(255))
    poster: Mapped[str] = mapped_column(String(255))
    translated_title: Mapped[str] = mapped_column(String(255))
    slogan: Mapped[str] = mapped_column(String(255))
    status_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))


class MovieGenre(Entity):
    __tablename__ = "movies_genres"

    genre_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class MoviePerson(Entity):
    __tablename__ = "movies_persons"

    activity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    person_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    @classmethod
    async def by_activity_id(
            cls,
            activity_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.activity_id == activity_id))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_person_id(
            cls,
            person_id: int,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.person_id == person_id))
        async for scalar in scalars:
            yield scalar


class MoviePlaylist(Entity):
    __tablename__ = "movies_playlists"

    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    playlist_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))


class MovieStudio(Entity):
    __tablename__ = "movies_studios"

    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    studio_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_studio_id(
            cls,
            studio_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.studio_id == studio_id))
        async for scalar in scalars:
            yield scalar


class MovieTag(Entity):
    __tablename__ = "movies_tags"

    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    relevance: Mapped[int]
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Person(Entity):
    __tablename__ = "persons"

    name: Mapped[str] = mapped_column(String(255))


class Playlist(Entity):
    __tablename__ = "playlists"

    title: Mapped[str] = mapped_column(String(255))


class Quality(Entity):
    __tablename__ = "qualities"

    resolution: Mapped[int]


class Rating(Entity):
    __tablename__ = "ratings"

    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    value: Mapped[int]


class Record(Entity):
    __tablename__ = "records"

    episode_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    filename: Mapped[str] = mapped_column(String(255))
    quality_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    @classmethod
    async def by_episode_id(
            cls,
            episode_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.episode_id == episode_id))
        async for scalar in scalars:
            yield scalar


class Review(Entity):
    __tablename__ = "reviews"

    content: Mapped[str] = mapped_column(Text)
    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Screenshot(Entity):
    __tablename__ = "screenshots"

    filename: Mapped[str] = mapped_column(String(255))
    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(255))

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Season(Entity):
    __tablename__ = "seasons"

    number: Mapped[int]
    movie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str] = mapped_column(String(255), nullable=True)

    @classmethod
    async def by_movie_id(
            cls,
            movie_id: uuid.UUID,
            session: AsyncSession,
    ):
        scalars = await session.stream_scalars(select(cls).where(cls.movie_id == movie_id))
        async for scalar in scalars:
            yield scalar


class Status(Entity):
    __tablename__ = "statuses"

    title: Mapped[str] = mapped_column(String(255))

class Studio(Entity):
    __tablename__ = "studios"

    title: Mapped[str] = mapped_column(String(255))


class Tag(Entity):
    __tablename__ = "tags"

    title: Mapped[str] = mapped_column(String(255))
