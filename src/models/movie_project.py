from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from ..database import Base
from ..schemas.movie_projects import Genre

class MovieProject(Base):
    __tablename__ = "movie_projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    budget = Column(Integer, default=0)
    genre = Column(String)
    outline = Column(Text)

    def generate_outline(self, db):
        me = db.query(MovieProject).filter(MovieProject.id == self.id).first()
        me.outline = "Generating outline..."
        db.commit()

        model = ChatOpenAI(model="gpt-4")

        prompt_template = ChatPromptTemplate.from_messages(
            [
               ("system", "You are a screenwriter starting a new project. You have been given the title '{title}' for a movie project and told that is in the {genre} genre. Please write a single paragraph outline for a potential story that would fit.")
            ]
        )
        
        parser = StrOutputParser()

        chain = prompt_template | model | parser

        result = chain.invoke({"title": me.title, "genre": me.genre})
        print("result", result)
        me.outline = result

        db.commit()
        return me
    
    def genre_values(self):
        return [element.value for element in Genre]
    
