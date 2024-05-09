from pydantic import BaseModel

from shared.schemas import EntityDBSchema


class MovieCreateSchema(BaseModel):
    title: str


class MovieDBSchema(MovieCreateSchema, EntityDBSchema):
    pass
