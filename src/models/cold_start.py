from pydantic import BaseModel


class Genre(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: str
    title: str
