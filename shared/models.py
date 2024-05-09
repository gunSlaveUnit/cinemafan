import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from root.models import Base


class Entity(Base):
    """
    Used as base class for all models
    with useful base fields
    like id, created_at, updated_at etc.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(onupdate=func.now())
