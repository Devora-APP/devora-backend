from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from fastapi import HTTPException
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.models.answer import Answer
from app.models.tag import Tag
from app.models.question_tag import question_tags
from app.utils.pagination import paginate


# Create Question
def create_question(db: Session, user_id, data: QuestionCreate):
    question = Question(
        title=data.title,
        body=data.body,
        language=data.language,
        user_id=user_id
    )

    db.add(question)
    db.flush()  

    # Attach tags
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()

        if len(tags) != len(data.tag_ids):
            raise HTTPException(status_code=400, detail="Invalid tag IDs")

        for tag in tags:
            db.execute(
                question_tags.insert().values(
                    question_id=question.id,
                    tag_id=tag.id
                )
            )

            tag.usage_count += 1

    db.commit()
    db.refresh(question)

    return question


# Get Questions
def get_questions(db, page=1, size=10, tag_id=None, language=None, sort="latest"):
    query = db.query(Question)

    # Filter by tag
    if tag_id:
        query = query.join(
            question_tags,
            Question.id == question_tags.c.question_id
        ).filter(question_tags.c.tag_id == tag_id)

    # Filter by language
    if language:
        query = query.filter(Question.language == language)

    # Sorting
    valid_sorts = ["latest", "most_voted", "most_viewed"]

    if sort and sort not in valid_sorts:
        raise HTTPException(
        status_code=400,
        detail="Invalid sort. Use: latest, most_voted, most_viewed"
    )
    if sort == "latest":
        query = query.order_by(desc(Question.created_at))

    elif sort == "most_voted":
        query = query.order_by(desc(Question.vote_count))

    elif sort == "most_viewed":
        query = query.order_by(desc(Question.view_count))

    else:
        query = query.order_by(desc(Question.created_at))

    return paginate(query, page, size)


# Get Question By Id
def get_question_by_id(db, question_id):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Increment view count
    question.view_count += 1

    db.commit()
    db.refresh(question)

    return question


# Update Questions
def update_question(db, question_id, user_id, data):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if data.title is not None:
        question.title = data.title
    if data.body is not None:
        question.body = data.body
    if data.language is not None:
        question.language = data.language

    db.commit()
    db.refresh(question)

    return question

# Delete Question
def delete_question(db, question_id, user_id):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(question)
    db.commit()

    return True


# Create Answer
def create_answer(db, user_id, data):
    question = db.query(Question).filter(Question.id == data.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    answer = Answer(
        body=data.body,
        question_id=data.question_id,
        user_id=user_id
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


# Get Answers for a Question
def get_answers_by_question(db, question_id, page=1, size=10):
    query = db.query(Answer).filter(Answer.question_id == question_id)

    return paginate(query, page, size)


# Update Answer
def update_answer(db, answer_id, user_id, data):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    if answer.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if data.body is not None:
        answer.body = data.body

    db.commit()
    db.refresh(answer)

    return answer


# Delete Answer
def delete_answer(db, answer_id, user_id):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    if answer.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(answer)
    db.commit()

    return True


# Accept Answer
def accept_answer(db, answer_id, user_id):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    question = db.query(Question).filter(Question.id == answer.question_id).first()

    if question.user_id != user_id:
        raise HTTPException(status_code=403, detail="Only question owner can accept")

    # reset previous accepted answers
    db.query(Answer).filter(Answer.question_id == question.id).update(
        {"is_accepted": False}
    )

    answer.is_accepted = True
    question.is_answered = True

    db.commit()
    db.refresh(answer)

    return answer