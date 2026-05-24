from pydantic import BaseModel
from uuid import UUID


class VoteRequest(BaseModel):
    target_id: UUID
    target_type: str  # "Question" or "Answer"
    value: int  # +1(Upvote), -1(Downvote), & 0(Remove vote)