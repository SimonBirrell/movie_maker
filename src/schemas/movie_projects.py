from pydantic import BaseModel
from enum import Enum

class Genre(str, Enum):
    action = "action"
    comedy = "comedy"
    drama = "drama"
    fantasy = "fantasy"
    horror = "horror"
    romance = "romance"
    scifi = "scifi"
    thriller = "thriller"

class MovieProjectBase(BaseModel):
    title: str
    genre: str = ""
    description: str = "Some rubbish"
    outline: str = ""
    budget: int = 1000000

class MovieProjectCreate(MovieProjectBase):
    pass

class MovieProjectRead(MovieProjectBase):
    id: int

class MovieProject(MovieProjectBase):
    id: int

    class Config:
        orm_mode = True