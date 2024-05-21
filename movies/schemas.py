import datetime

from pydantic import BaseModel

from shared.schemas import EntityDBSchema


class PersonCreateSchema(BaseModel):
    name: str


class PersonDBSchema(PersonCreateSchema, EntityDBSchema):
    pass


class ActionCreateSchema(BaseModel):
    title: str


class ActionDBSchema(ActionCreateSchema, EntityDBSchema):
    pass


class MoviePersonCreateSchema(BaseModel):
    movie_id: int
    person_id: int
    activity_id: int


class AgeCreateSchema(BaseModel):
    title: str
    description: str


class AgeDBSchema(AgeCreateSchema, EntityDBSchema):
    pass


class CategoryCreateSchema(BaseModel):
    title: str


class CategoryDBSchema(CategoryCreateSchema, EntityDBSchema):
    pass


class MovieCreateSchema(BaseModel):
    translated_title: str
    original_title: str
    poster: str
    description: str
    age_id: int
    category_id: int


class MovieDBSchema(MovieCreateSchema, EntityDBSchema):
    pass


class GenreCreateSchema(BaseModel):
    title: str


class GenreDBSchema(GenreCreateSchema, EntityDBSchema):
    pass


class MovieGenreCreateSchema(BaseModel):
    movie_id: int
    genre_id: int


class MovieGenreDBSchema(MovieGenreCreateSchema, EntityDBSchema):
    pass


class TagCreateSchema(BaseModel):
    title: str


class TagDBSchema(TagCreateSchema, EntityDBSchema):
    pass


class TaggingCreateSchema(BaseModel):
    movie_id: int
    tag_id: int


class TaggingDBSchema(TaggingCreateSchema, EntityDBSchema):
    pass


class SeasonCreateSchema(BaseModel):
    number: int
    title: str | None = None
    movie_id: int


class SeasonDBSchema(SeasonCreateSchema, EntityDBSchema):
    pass


class EpisodeCreateSchema(BaseModel):
    release_date: datetime.datetime
    number: int
    parent_id: int | None = None
    season_id: int
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


class ScreenshotCreateSchema(BaseModel):
    title: str
    movie_id: int
    filename: str


class ScreenshotDBSchema(ScreenshotCreateSchema, EntityDBSchema):
    pass
