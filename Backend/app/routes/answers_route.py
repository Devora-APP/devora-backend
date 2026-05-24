from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.answer import (AnswerCreate, AnswerResponse, AnswerUpdate)
from app.schemas.pagination import PaginatedResponse
from app.services.qa_service import (
    create_answer,
    get_answers_by_question,
    update_answer,
    delete_answer,
    accept_answer
)

router = APIRouter(prefix="/answers", tags=["Answers"])


# Create Answer
@router.post("/", response_model=AnswerResponse)
def create_new_answer(
    data: AnswerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_answer(db, current_user.id, data)


# Get Answers by Question
@router.get("/question/{question_id}", response_model=PaginatedResponse[AnswerResponse])
def get_answers(
    question_id,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    return get_answers_by_question(db, question_id, page, size)


# Update Answer
@router.put("/{answer_id}", response_model=AnswerResponse)
def update_existing_answer(
    answer_id,
    data: AnswerUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_answer(db, answer_id, current_user.id, data)


# Delete Answer
@router.delete("/{answer_id}")
def delete_existing_answer(
    answer_id,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_answer(db, answer_id, current_user.id)
    return {"message": "Answer deleted"}


# Accept Answer
@router.post("/{answer_id}/accept", response_model=AnswerResponse)
def accept_existing_answer(
    answer_id,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return accept_answer(db, answer_id, current_user.id)