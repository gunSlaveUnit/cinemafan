import datetime

from sqlalchemy import String, ForeignKey, select, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class Age(Entity):
    __tablename__ = "ages"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)


class Movie(Entity):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    age_id: Mapped[int] = mapped_column(ForeignKey("ages.id"))


class Episode(Entity):
    __tablename__ = "episodes"

    release_date: Mapped[datetime.datetime]
    movie_id: Mapped[int]
    number: Mapped[int]
    parent_id: Mapped[int] = mapped_column(ForeignKey("episodes.id"), nullable=True)
    season: Mapped[int]
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
