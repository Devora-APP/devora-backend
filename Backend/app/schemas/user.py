from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

#  Base
class UserBase(BaseModel):
    username: str
    email: EmailStr


#  For response
class UserResponse(UserBase):
    id: UUID
    avatar_url: str | None
    reputation: int
    created_at: datetime

    class Config:
        from_attributes = True


#  For updating profile
class UserUpdate(BaseModel):
    username: str | None = None
    avatar_url: str | None = None