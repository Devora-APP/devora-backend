import uuid
from sqlalchemy import Column, Text, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    target_id = Column(UUID(as_uuid=True), nullable=False)
    target_type = Column(String, nullable=False)  # "question" or "answer"

    body = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())