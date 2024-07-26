from sqlalchemy.orm import Session

from . import schemas, models

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