from sqlalchemy.orm import Mapped, mapped_column

from root.models import Base


class Entity(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
