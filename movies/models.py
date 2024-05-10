from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class Movie(Entity):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(255))


class Episode(Entity):
    __tablename__ = "episodes"

    movie_id: Mapped[int] = mapped_column()
    number: Mapped[int] = mapped_column()
    parent_id: Mapped[int] = mapped_column(ForeignKey("episodes.id"))
    season: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column(String(255))
