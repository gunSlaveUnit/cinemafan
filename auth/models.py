from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class User(Entity):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
