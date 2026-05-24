from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.user import UserResponse
from app.services.user_service import get_all_users
from app.core.security import get_current_user
from app.schemas.user import UserUpdate
from app.services.user_service import (
    get_user_by_id, update_user, get_user_stats)
from app.schemas.pagination import PaginatedResponse
from app.schemas.question import QuestionResponse
from app.services.user_service import get_user_questions
from app.schemas.answer import AnswerResponse
from app.services.user_service import get_user_answers


router = APIRouter(prefix="/users", tags=["Users"])


# Get All Users List
@router.get("/", response_model=PaginatedResponse[UserResponse])
def list_users(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    return get_all_users(db, page, size)


# Get user profile by id
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


# Update user profile
@router.put("/{user_id}", response_model=UserResponse)
def update_user_profile(
    user_id,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_user(db, user_id, current_user.id, data)


# Get list of question created by user
@router.get("/{user_id}/questions", response_model=PaginatedResponse[QuestionResponse])
def user_questions(
    user_id,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    return get_user_questions(db, user_id, page, size)


# Get list of answers created by user
@router.get("/{user_id}/answers", response_model=PaginatedResponse[AnswerResponse])
def user_answers(
    user_id,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    return get_user_answers(db, user_id, page, size)


# User Stats
@router.get("/{user_id}/stats")
def user_stats(user_id, db: Session = Depends(get_db)):
    return get_user_stats(db, user_id)