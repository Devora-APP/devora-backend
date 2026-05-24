from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.vote import VoteRequest
from app.services.vote_service import vote

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/")
def vote_api(
    data: VoteRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return vote(db, current_user.id, data)