import uuid
from sqlalchemy import (
    Column,
    String, 
    Text, 
    Integer, 
    Boolean, 
    DateTime, 
    ForeignKey
    )
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.base import Base
from app.models.question_tag import question_tags
from app.models.tag import Tag


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    title = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)

    language = Column(String(30), nullable=False)

    view_count = Column(Integer, default=0)
    vote_count = Column(Integer, default=0)

    is_answered = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    tags = relationship("Tag", secondary=question_tags, back_populates="questions")