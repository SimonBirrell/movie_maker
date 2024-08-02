from sqlalchemy.orm import Session

from . import schemas, models

# Movie Project CRUD

def get_movie_project(db: Session, movie_project_id: int):
    db_movie_project = db.query(models.MovieProject).filter(models.MovieProject.id == movie_project_id).first()
    print("Retrieved movie_project", db_movie_project.genre, db_movie_project.outline)
    return db_movie_project

def get_movie_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MovieProject).offset(skip).limit(limit).all()

def create_movie_project(db: Session, movie_project: schemas.MovieProjectCreate):
    db_movie_project = models.MovieProject(
        title=movie_project.title, 
        description=movie_project.description,
        outline=movie_project.outline,
        genre=movie_project.genre,
        budget=movie_project.budget
        )
    db.add(db_movie_project)
    db.commit()
    db.refresh(db_movie_project)
    return db_movie_project

def save_movie_project(db: Session, movie_project: schemas.MovieProject):
    db_movie_project = db.query(models.MovieProject).filter(models.MovieProject.id == movie_project.id).first()
    db_movie_project.title = movie_project.title
    db_movie_project.description = movie_project.description
    db_movie_project.outline = movie_project.outline
    db_movie_project.genre = movie_project.genre
    db_movie_project.budget = movie_project.budget
    print("Committing changes", db_movie_project.genre, db_movie_project.outline)
    db.commit()
    db.refresh(db_movie_project)
    print("Committing changes", db_movie_project.genre, db_movie_project.outline)
    return db_movie_project

# Cast Member CRUD

def get_cast_member(db: Session, cast_member_id: int):
    return db.query(models.CastMember).filter(models.CastMember.id == cast_member_id).first()

def get_cast_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CastMember).offset(skip).limit(limit).all()

def get_cast_members_on_movie_project(db: Session, movie_project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.CastMember).filter(models.CastMember.movie_project_id == movie_project_id).offset(skip).limit(limit).all()

def create_cast_member(db: Session, cast_member: schemas.CastMemberCreate):
    db_cast_member = models.CastMember(
        movie_project_id=cast_member.movie_project_id, 
        character_name=cast_member.character_name,
        actor_name=cast_member.actor_name,
        justification_for_actor=cast_member.justification_for_actor
        )
    db.add(db_cast_member)
    db.commit()
    db.refresh(db_cast_member)
    return db_cast_member

def save_cast_member(db: Session, cast_member: schemas.CastMember):
    db_cast_member = db.query(models.CastMember).filter(models.CastMember.id == cast_member.id).first()
    db_cast_member.character_name = cast_member.character_name
    db_cast_member.actor_name = cast_member.actor_name
    db_cast_member.justification_for_actor = cast_member.justification_for_actor
    db.commit()
    db.refresh(db_cast_member)
    return db_cast_member

def delete_cast_member(db: Session, cast_member_id: int):
    db.query(models.CastMember).filter(models.CastMember.id == cast_member_id).delete()
    db.commit()
    return {"status": "success"}

