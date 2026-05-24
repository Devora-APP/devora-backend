from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.tag import Tag


def create_tag(db: Session, data):
    existing = db.query(Tag).filter(Tag.name == data.name).first()

    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    tag = Tag(name=data.name, description=data.description)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def get_tags(db: Session):
    return db.query(Tag).all()