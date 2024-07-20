import datetime

from pydantic import BaseModel


class EntityDBSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True
