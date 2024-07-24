from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...schemas.movie_projects import MovieProjectBase
from ...database import get_db
from ... import crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/movie_project", tags=['API'])
async def create_movie_project(movie_project: MovieProjectBase, db: Session = Depends(get_db)):
    return crud.create_movie_project(db=db, movie_project=movie_project)

@router.get("/movie_project/{movie_project_id}", tags=['API'])
async def read_movie_project(movie_project_id: int, db: Session = Depends(get_db)):
    movie_project = crud.get_movie_project(db=db, movie_project_id=movie_project_id)
    if movie_project is None:
        raise HTTPException(status_code=404, detail=f"Movie Project ID={movie_project_id} not found")
    return movie_project
