from pydantic import BaseModel

from shared.schemas import EntityDBSchema


class MovieCreateSchema(BaseModel):
    title: str


class MovieDBSchema(MovieCreateSchema, EntityDBSchema):
    pass


class EpisodeCreateSchema(BaseModel):
    movie_id: int
    number: int
    parent_id: int | None = None
    season: int
    title: str


class EpisodeDBSchema(EpisodeCreateSchema, EntityDBSchema):
    pass


class QualityCreateSchema(BaseModel):
    resolution: int
