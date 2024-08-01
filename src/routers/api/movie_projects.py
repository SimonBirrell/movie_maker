from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
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

@router.post("/movie_projects/{movie_project_id}/generate_outline", tags=['API'])
async def ui_generate_outline_for_movie_project(                                
                                request: Request, 
                                movie_project_id: int, 
                                background_tasks: BackgroundTasks,
                                db: Session = Depends(get_db)
                                ):
    movie_project = crud.get_movie_project(db=db, movie_project_id=movie_project_id)
    if movie_project is None:
        raise HTTPException(status_code=404, detail=f"Movie Project ID={movie_project_id} not found")
    movie_project.outline = "Generating outline... please refresh in a few seconds..."
    db.commit()
    db.refresh(movie_project)
    background_tasks.add_task(movie_project.generate_outline, db)
    return movie_project