from pydantic import BaseModel

class MovieProjectBase(BaseModel):
    title: str
    description: str = "Some rubbish"
    budget: int = 1000000

class MovieProjectCreate(MovieProjectBase):
    pass

class MovieProjectRead(MovieProjectBase):
    id: int

class MovieProject(MovieProjectBase):
    id: int

    class Config:
        orm_mode = True