import asyncio, json

from fastapi import APIRouter, Depends, HTTPException, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse
from typing import Annotated
from sqlalchemy.orm import Session

from ...schemas.movie_projects import MovieProjectBase, Genre
from ...database import get_db
from ... import crud
from ...models import team_contribution_queue

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/ui/movie_projects", response_class=HTMLResponse, tags=['UI'])
async def ui_root(request: Request, db: Session = Depends(get_db)) -> str:
   return templates.TemplateResponse(
        request=request, name="movie_projects/index.html", context={
            "movie_projects": crud.get_movie_projects(db=db)
        }
    )

@router.get("/ui/movie_projects/{movie_project_id}", response_class=HTMLResponse, tags=['UI'])
async def ui_read_movie_project(request: Request, movie_project_id: int, db: Session = Depends(get_db)):
    movie_project = crud.get_movie_project(db=db, movie_project_id=movie_project_id)
    if movie_project is None:
        raise HTTPException(status_code=404, detail=f"Movie Project ID={movie_project_id} not found")
    return templates.TemplateResponse(
        request=request, name="movie_projects/show.html", context={"movie_project": movie_project}
    )

@router.get("/ui/movie_projects/{movie_project_id}/edit", response_class=HTMLResponse, tags=['UI'])
async def ui_read_movie_project(request: Request, movie_project_id: int, db: Session = Depends(get_db)):
    movie_project = crud.get_movie_project(db=db, movie_project_id=movie_project_id)
    if movie_project is None:
        raise HTTPException(status_code=404, detail=f"Movie Project ID={movie_project_id} not found")
    return templates.TemplateResponse(
        request=request, name="movie_projects/edit.html", context={"movie_project": movie_project}
    )

@router.post("/ui/movie_projects/{movie_project_id}", response_class=HTMLResponse, tags=['UI'])
async def ui_post_movie_project(                                
                                request: Request, 
                                movie_project_id: int, 
                                title: Annotated[str, Form()],
                                genre: Annotated[Genre, Form()] = "",
                                description: Annotated[str, Form()] = "",
                                outline: Annotated[str, Form()] = "",
                                db: Session = Depends(get_db)
                                ):
    movie_project = crud.get_movie_project(db=db, movie_project_id=movie_project_id)
    movie_project.title = title
    movie_project.genre = genre
    movie_project.description = description
    movie_project.outline = outline
    movie_project = crud.save_movie_project(db, movie_project)

    if movie_project is None:
        raise HTTPException(status_code=404, detail=f"Movie Project ID={movie_project_id} not found")
    return templates.TemplateResponse(
        request=request, name="movie_projects/show.html", context={"movie_project": movie_project}
    )

@router.get("/team_contributions")
async def live_team_contributions():
    print("Setting up live_team_contributions")
    print("Team_contribution_queue", team_contribution_queue.queue)
    if team_contribution_queue.queue is None:
        raise HTTPException(status_code=500, detail="Team_contribution_queue is not initialized!")

    print("queue", team_contribution_queue.queue)
    async def generate_stream():
        try:
            while True:
                # await asyncio.sleep(1) # waits for a second
                # payload = json.dumps({'movie_project_id': 2, 'name': "Jo Schmoe", 'contribution': "Critiqued the first draft outline"})
                print("Waiting for a team contribution...")
                payload = await team_contribution_queue.queue.get() # receives an update from queue
                print("Got a team contribution!", payload)
                yield dict(data=json.dumps(payload), event="team-contribution") # sends it to the browser
        except asyncio.CancelledError as e:
            # when the browser disconects, cancels notifications
            raise e

    print("Returning stream...")
    return EventSourceResponse(generate_stream())