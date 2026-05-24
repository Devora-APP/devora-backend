from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
from app.schemas.tag import TagResponse


#  Create Question 
class QuestionCreate(BaseModel):
    title: str
    body: str
    language: str
    tag_ids: list[UUID] = []


# Update Question
class QuestionUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    language: str | None = None


#  Response 
class QuestionResponse(BaseModel):
    id: UUID
    title: str
    body: str
    language: str

    vote_count: int
    view_count: int
    is_answered: bool

    created_at: datetime
    user_id: UUID

    tags: List[TagResponse] = []
    
    class Config:
        from_attributes = True