from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import get_db

from .schemas.movie_projects import MovieProjectRead
from .routers.movie_projects import router as movie_projects_router
from . import crud

app = FastAPI()

@app.get("/")
async def root(db: Session = Depends(get_db)) -> list[MovieProjectRead]:
    return crud.get_movie_projects(db=db)

app.include_router(movie_projects_router)