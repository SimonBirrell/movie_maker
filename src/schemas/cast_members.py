from pydantic import BaseModel

class CastMemberBase(BaseModel):
    movie_project_id: int = 0
    character_name: str = ""
    actor_name: str = ""
    justification_for_actor: str = ""

class CastMemberCreate(CastMemberBase):
    pass

class CastMember(CastMemberBase):
    id: int

    class Config:
        orm_mode = True
