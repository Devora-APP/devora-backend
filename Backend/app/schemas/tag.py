from pydantic import BaseModel
from uuid import UUID


class TagCreate(BaseModel):
    name: str
    description: str | None = None


class TagResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    usage_count: int

    class Config:
        from_attributes = True