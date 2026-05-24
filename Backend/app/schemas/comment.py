from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class CommentCreate(BaseModel):
    body: str
    target_id: UUID
    target_type: str  # "question" or "answer"


class TargetType(str, Enum):
    question = "question"
    answer = "answer"

class CommentResponse(BaseModel):
    id: UUID
    body: str
    user_id: UUID
    target_id: UUID
    target_type: TargetType
    created_at: datetime

    class Config:
        from_attributes = True