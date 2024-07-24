from sqlalchemy.orm import Session

from . import schemas, models

def get_movie_project(db: Session, movie_project_id: int):
    return db.query(models.MovieProject).filter(models.MovieProject.id == movie_project_id).first()

def get_movie_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MovieProject).offset(skip).limit(limit).all()

def create_movie_project(db: Session, movie_project: schemas.MovieProjectCreate):
    db_movie_project = models.MovieProject(
        title=movie_project.title, 
        description=movie_project.description,
        budget=movie_project.budget
        )
    db.add(db_movie_project)
    db.commit()
    db.refresh(db_movie_project)
    return db_movie_project

