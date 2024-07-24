from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.movie_projects import MovieProjectBase
from ..database import get_db
from .. import crud

router = APIRouter()

@router.post("/movie_project")
async def create_movie_project(movie_project: MovieProjectBase, db: Session = Depends(get_db)):
    return crud.create_movie_project(db=db, movie_project=movie_project)

@router.get("/movie_project/{movie_project_id}")
async def read_movie_project(movie_project_id: int, db: Session = Depends(get_db)):
    movie_project = crud.get_movie_project(db=db, movie_project_id=movie_project_id)
    if movie_project is None:
        raise HTTPException(status_code=404, detail=f"Movie Project ID={movie_project_id} not found")
    return movie_project
