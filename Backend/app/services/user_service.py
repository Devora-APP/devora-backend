from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from app.models.vote import Vote
from app.utils.pagination import paginate


# Get all users
def get_all_users(db: Session, page=1, size=10):
    query = db.query(User)
    return paginate(query, page, size)


# Get user by ID
def get_user_by_id(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Update user
def update_user(db, user_id, current_user_id, data):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only user can update the profile
    if user.id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Check if the username already exists
    if data.username:
        existing_user = db.query(User).filter(
            User.username == data.username
        ).first()

        if existing_user and existing_user.id != user_id:
            raise HTTPException(400, "Username already taken")

    if data.username is not None:
        user.username = data.username

    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url

    db.commit()
    db.refresh(user)

    return user


# Get all Questions by user
def get_user_questions(db, user_id, page=1, size=10):
    query = db.query(Question).filter(Question.user_id == user_id)

    return paginate(query, page, size)


# Get all Answers by user
def get_user_answers(db, user_id, page=1, size=10):
    query = db.query(Answer).filter(Answer.user_id == user_id)

    return paginate(query, page, size)


# User stats
def get_user_stats(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    questions_count = db.query(Question).filter(Question.user_id == user_id).count()

    answers_count = db.query(Answer).filter(Answer.user_id == user_id).count()

    accepted_answers = db.query(Answer).filter(
        Answer.user_id == user_id,
        Answer.is_accepted == True
    ).count()

    # Votes on user's questions
    question_votes = db.query(Vote).join(
        Question,
        Vote.target_id == Question.id
    ).filter(
        Vote.target_type == "question",
        Question.user_id == user_id
        ).count()

    # Votes on user's answers
    answer_votes = db.query(Vote).join(
        Answer,
        Vote.target_id == Answer.id
    ).filter(
        Vote.target_type == "answer",
        Answer.user_id == user_id
    ).count()

    total_votes_received = question_votes + answer_votes

    return {
        "questions": questions_count,
        "answers": answers_count,
        "accepted_answers": accepted_answers,
        "total_votes_received": total_votes_received,
        "reputation": user.reputation
    }