import asyncio

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from ..database import Base
from ..schemas.movie_projects import Genre
from ..models import team_contribution_queue

class MovieProject(Base):
    __tablename__ = "movie_projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    budget = Column(Integer, default=0)
    genre = Column(String)
    outline = Column(Text)

    async def generate_outline(self, db):
        me = db.query(MovieProject).filter(MovieProject.id == self.id).first()
        me.outline = "Generating outline..."
        db.commit()

        for i in range(1):
            await self.studio_exec_start()
            await asyncio.sleep(5)

        me.outline = await self.first_draft_outline(me.title, me.genre)
        db.commit()
        
        print("Critiquing outline")
        critique = await self.critique_outline(me.title, me.genre, me.outline)
        print(critique)

        me.outline = await self.second_draft_outline(me.title, me.genre, me.outline, critique)

        db.commit()
        return me
    
    async def studio_exec_start(self):
        await team_contribution_queue.add_contribution_to_queue(self.id, "Studio Exec", "Get cracking!!!")
    
    async def first_draft_outline(self, title, genre):
        return await self.generate_contribution("You are a talented screenwriter starting a new project. You have been given the title '{title}' for a movie project and told that is in the {genre} genre. Please write a single paragraph outline for a potential story that would fit.", "Junior Screenwriter", title, genre)
    
    async def critique_outline(self, title, genre, outline):
        return await self.generate_contribution("You are a very experienced and commercially successful screenwriter who has been handed a first draft outline for a movie project. Please give some constructive criticism that the screenwriter can use to improve and flesh out the outline. Movie Title: {title} Movie Genre: {genre} Outline: {outline}", "Senior Screenwriter", title, genre, outline=outline)
    
    async def second_draft_outline(self, title, genre, outline, critique):
        return await self.generate_contribution("You are a talented screenwriter working a new project. You have been given the title '{title}' for a movie project, told that is in the {genre} genre and you've generated a possible outline for the story, shown below. Your boss, an experienced screenwriter, has given you a critique below. Please rewrite the outline based on the suggestions in the critique.\n\n Your Outline:\n{outline}\n\n Your boss's critique:\n{critique}", "Junior Screenwriter", title, genre, outline=outline, critique=critique)
    
    async def generate_contribution(self, prompt_text, name, title, genre, outline="", critique=""):
        global Team_contribution_queue
        model = ChatOpenAI(model="gpt-4")
        prompt_template = ChatPromptTemplate.from_messages(
            [
               ("system", prompt_text)
            ]
        )    
        parser = StrOutputParser()
        chain = prompt_template | model | parser
        result = await chain.ainvoke({"title": title, "genre": genre, "outline": outline, "critique": critique})
        if team_contribution_queue.queue is None:
            raise("team_contribution_queue.queue is not initialized!")
        else:
            await team_contribution_queue.add_contribution_to_queue(self.id, name, result)
        return result
        
    def genre_values(self):
        return [element.value for element in Genre]
    
