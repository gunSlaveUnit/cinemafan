from pydantic import BaseModel


class MovieCreateSchema(BaseModel):
    title: str
