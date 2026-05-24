from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


#  Create Answer
class AnswerCreate(BaseModel):
    body: str
    question_id: UUID


#  Update Answer
class AnswerUpdate(BaseModel):
    body: str | None = None


#  Response
class AnswerResponse(BaseModel):
    id: UUID
    body: str

    question_id: UUID
    user_id: UUID

    vote_count: int
    is_accepted: bool

    created_at: datetime

    class Config:
        from_attributes = True