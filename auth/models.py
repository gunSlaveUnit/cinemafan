from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared.models import Entity


class User(Entity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(255))
