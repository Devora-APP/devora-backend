import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.question_tag import question_tags
from app.core.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(50), unique=True, nullable=False)
    description = Column(String, nullable=True)

    usage_count = Column(Integer, default=0)

    # Relationships
    questions = relationship("Question", secondary=question_tags, back_populates="tags")