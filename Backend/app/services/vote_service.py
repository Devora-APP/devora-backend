from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.vote import Vote
from app.models.question import Question
from app.models.answer import Answer
from app.models.user import User


def vote(db: Session, user_id, data):
    if data.value not in [0, 1, -1]:
        raise HTTPException(status_code=400, detail="Invalid vote value")

    # Check existing vote
    existing_vote = db.query(Vote).filter(
        Vote.user_id == user_id,
        Vote.target_id == data.target_id,
        Vote.target_type == data.target_type
    ).first()

    # Get target
    if data.target_type == "question":
        target = db.query(Question).filter(Question.id == data.target_id).first()
    elif data.target_type == "answer":
        target = db.query(Answer).filter(Answer.id == data.target_id).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid target type")

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    # Prevent self voting
    if target.user_id == user_id:
        raise HTTPException(status_code=403, detail="You cannot vote on your own content")

    owner = db.query(User).filter(User.id == target.user_id).first()

    # Prevent voting other than question/answer
    if data.target_type not in ["question", "answer"]:
        raise HTTPException(status_code=400, detail="Invalid target type")

    # CASE 1: REMOVE VOTE
    if data.value == 0:
        if not existing_vote:
            return {"message": "No vote to remove"}

        # remove effect
        target.vote_count -= existing_vote.value

        # remove reputation
        if data.target_type == "answer":
            owner.reputation -= 5 * existing_vote.value
        elif data.target_type == "question":
            owner.reputation -= 2 * existing_vote.value

        db.delete(existing_vote)

        db.commit()
        return {"message": "Vote removed"}

    # CASE 2: UPDATE EXISTING VOTE
    if existing_vote:
        # remove old effect
        target.vote_count -= existing_vote.value

        if data.target_type == "answer":
            owner.reputation -= 5 * existing_vote.value
        elif data.target_type == "question":
            owner.reputation -= 2 * existing_vote.value

        # apply new vote
        existing_vote.value = data.value

    else:
        new_vote = Vote(
            user_id=user_id,
            target_id=data.target_id,
            target_type=data.target_type,
            value=data.value
        )
        db.add(new_vote)

    # apply new effect
    target.vote_count += data.value

    if data.target_type == "answer":
        owner.reputation += 5 * data.value
    elif data.target_type == "question":
        owner.reputation += 2 * data.value

    db.commit()
    db.refresh(target)

    return {"message": "Vote recorded"}