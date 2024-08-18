from pydantic import BaseModel


class MomentCreateSchema(BaseModel):
    content: str
    episode_id: int
    time: float


class ReviewCreateSchema(BaseModel):
    content: str
    movie_id: int
