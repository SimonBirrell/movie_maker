from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..database import Base

class MovieProject(Base):
    __tablename__ = "movie_projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    budget = Column(Integer, default=0)
    genre = Column(String)
    outline = Column(Text)

