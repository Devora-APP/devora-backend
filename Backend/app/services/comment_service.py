from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.comment import Comment
from app.models.question import Question
from app.models.answer import Answer
from app.utils.pagination import paginate


# Create comments 
def create_comment(db: Session, user_id, data):
    # Validate target
    if data.target_type == "question":
        target = db.query(Question).filter(Question.id == data.target_id).first()
    elif data.target_type == "answer":
        target = db.query(Answer).filter(Answer.id == data.target_id).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid target type")

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    comment = Comment(
        body=data.body,
        user_id=user_id,
        target_id=data.target_id,
        target_type=data.target_type
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# Get Comments
def get_comments(db: Session, target_id, target_type, page=1, size=10):
    if target_type not in ["question", "answer"]:
        raise HTTPException(status_code=400, detail="Invalid target_type")
    
    query = db.query(Comment).filter(
        Comment.target_id == target_id,
        Comment.target_type == target_type
    )

    return paginate(query, page, size)