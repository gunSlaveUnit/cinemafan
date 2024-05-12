from pydantic import BaseModel

from shared.schemas import EntityDBSchema


class AgeCreateSchema(BaseModel):
    title: str
    description: str


class AgeDBSchema(AgeCreateSchema, EntityDBSchema):
    pass


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


class QualityDBSchema(QualityCreateSchema, EntityDBSchema):
    pass


class RecordCreateSchema(BaseModel):
    episode_id: int
    quality_id: int
    filename: str


class RecordDBSchema(RecordCreateSchema, EntityDBSchema):
    pass
