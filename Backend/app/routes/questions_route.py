from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.qa_service import (
    create_question,
    get_questions,
    get_question_by_id,
    update_question,
    delete_question
)

router = APIRouter(prefix="/questions", tags=["Questions"])


#  Create Question
@router.post("/", response_model=QuestionResponse)
def create_new_question(
    data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_question(db, current_user.id, data)


#  Get All Questions
@router.get("/", response_model=PaginatedResponse[QuestionResponse])
def list_questions(
    page: int = 1,
    size: int = 10,
    tag_id: str | None = None,
    language: str | None = None,
    sort: str = "latest",
    db: Session = Depends(get_db)
):
    return get_questions(db, page, size, tag_id, language, sort)


#  Get Question by ID
@router.get("/{question_id}", response_model=QuestionResponse)
def get_single_question(
    question_id: UUID,
    db: Session = Depends(get_db)
):
    question = get_question_by_id(db, question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question


# Update Question
@router.put("/{question_id}", response_model=QuestionResponse)
def update_existing_question(
    question_id: UUID,
    data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_question(db, question_id, current_user.id, data)
    
# Delete Question
@router.delete("/{question_id}")
def delete_existing_question(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_question(db, question_id, current_user.id)
    return {"message": "Question deleted"}