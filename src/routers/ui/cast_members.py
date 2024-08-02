from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from ...schemas.cast_members import CastMember, CastMemberBase, CastMemberCreate
from ...database import get_db
from ... import crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/ui/cast_members", response_class=HTMLResponse, tags=['UI'])
async def ui_cast_members(request: Request, db: Session = Depends(get_db)) -> str:
   return templates.TemplateResponse(
        request=request, name="cast_members/index.html", context={
            "cast_members": crud.get_cast_members(db=db)
        }
    )

@router.get("/ui/cast_members/new", response_class=HTMLResponse, tags=['UI'])
async def ui_new_cast_member(request: Request, db: Session = Depends(get_db)):
    movie_projects = crud.get_movie_projects(db=db)
    cast_member = CastMemberBase()
    return templates.TemplateResponse(
        request=request, name="cast_members/edit.html", context={"cast_member": cast_member, "movie_projects": movie_projects}
    )

@router.post("/ui/cast_members/", response_class=HTMLResponse, tags=['UI'])
async def ui_post_new_cast_member(
        request: Request, 
        movie_project_id: Annotated[int, Form()],
        character_name: Annotated[str, Form()],
        actor_name: Annotated[str, Form()] = "",
        justification_for_actor: Annotated[str, Form()] = "",
        db: Session = Depends(get_db)
    ):
    print("Creating cast member", movie_project_id, character_name, actor_name, justification_for_actor)
    cast_member = CastMemberCreate(movie_project_id=movie_project_id, character_name=character_name, actor_name=actor_name, justification_for_actor=justification_for_actor)
    db_cast_member = crud.create_cast_member(db, cast_member=cast_member)
    if cast_member is None:
        raise HTTPException(status_code=404, detail=f"Cast Member ID={cast_member_id} not found")
    return templates.TemplateResponse(
        request=request, name="cast_members/show.html", context={"cast_member": db_cast_member}
    )


@router.get("/ui/cast_members/{cast_member_id}", response_class=HTMLResponse, tags=['UI'])
async def ui_read_cast_member(request: Request, cast_member_id: int, db: Session = Depends(get_db)):
    cast_member = crud.get_cast_member(db=db, cast_member_id=cast_member_id)
    movie_project = crud.get_movie_project(db=db, movie_project_id=cast_member.movie_project_id)
    if cast_member is None:
        raise HTTPException(status_code=404, detail=f"Cast Member ID={cast_member_id} not found")
    return templates.TemplateResponse(
        request=request, name="cast_members/show.html", context={"cast_member": cast_member, "movie_project": movie_project}
    )

@router.get("/ui/cast_members/{cast_member_id}/edit", response_class=HTMLResponse, tags=['UI'])
async def ui_edit_cast_member(request: Request, cast_member_id: int, db: Session = Depends(get_db)):
    cast_member = crud.get_cast_member(db=db, cast_member_id=cast_member_id)
    if cast_member is None:
        raise HTTPException(status_code=404, detail=f"Cast Member ID={cast_member_id} not found")
    return templates.TemplateResponse(
        request=request, name="cast_members/edit.html", context={"cast_member": cast_member}
    )

@router.post("/ui/cast_members/{cast_member_id}", response_class=HTMLResponse, tags=['UI'])
async def ui_post_cast_member(request: Request, cast_member: CastMember, db: Session = Depends(get_db)):
    cast_member = crud.create_cast_member(db, cast_member=cast_member)
    if cast_member is None:
        raise HTTPException(status_code=404, detail=f"Cast Member ID={cast_member_id} not found")
    return templates.TemplateResponse(
        request=request, name="cast_members/show.html", context={"cast_member": cast_member}
    )

