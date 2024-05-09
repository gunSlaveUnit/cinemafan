import datetime
from typing import Optional

from pydantic import BaseModel


class EntityDBSchema(BaseModel):
    """
    Entity validation schema.
    Used to other API schemas as a base class.
    """

    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True
