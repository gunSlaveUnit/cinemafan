from pydantic import BaseModel

from shared.schemas import EntityDBSchema


class ReviewCreateSchema(BaseModel):
	content: str
	movie_id: int
