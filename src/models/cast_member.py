import asyncio

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from ..database import Base
from ..schemas.movie_projects import Genre

class CastMember(Base):
    __tablename__ = "cast_members"

    id = Column(Integer, primary_key=True)
    movie_project_id = Column(Integer, ForeignKey("movie_projects.id"))
    character_name = Column(String, index=True)
    actor_name = Column(String)
    justification_for_actor = Column(String)
