from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    """
    Base class to work with SQLAlchemy functionality.
    Primarily used for Entity class.
    """

    pass
