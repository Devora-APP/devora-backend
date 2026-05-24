from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import create_comment, get_comments
from app.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


# Create Comment
@router.post("/", response_model=CommentResponse)
def create_new_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_comment(db, current_user.id, data)


# Get Comments
@router.get("/", response_model=PaginatedResponse[CommentResponse])
def list_comments(
    target_id: str,
    target_type: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    return get_comments(db, target_id, target_type, page, size)