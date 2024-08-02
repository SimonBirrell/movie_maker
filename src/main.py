from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .database import get_db

from .schemas.movie_projects import MovieProjectRead
from .routers.api.movie_projects import router as api_movie_projects_router
from .routers.ui.movie_projects import router as ui_movie_projects_router
from .routers.ui.cast_members import router as ui_cast_members_router
from . import crud

#from .models.team_contribution_queue import startup as team_contribution_queue_startup
#
#team_contribution_queue_startup()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=['API'])
async def root(db: Session = Depends(get_db)) -> list[MovieProjectRead]:
    return crud.get_movie_projects(db=db)

@app.get("/ui/", response_class=HTMLResponse, tags=['UI'])
async def ui_root(request: Request, db: Session = Depends(get_db)) -> str:
   return templates.TemplateResponse(
        request=request, name="home.html", context={
            "movie_projects": crud.get_movie_projects(db=db)
        }
    )

app.include_router(api_movie_projects_router)
app.include_router(ui_movie_projects_router)
app.include_router(ui_cast_members_router)
