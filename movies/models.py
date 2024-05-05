from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..shared.models import Entity


class Movie(Entity):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(255))
