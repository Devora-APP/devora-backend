import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.core.base import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    target_id = Column(UUID(as_uuid=True), nullable=False)
    target_type = Column(String, nullable=False)  # "question" or "answer"

    # +1 or -1
    value = Column(Integer, nullable=False)  

    __table_args__ = (
        UniqueConstraint("user_id", "target_id", "target_type", name="unique_vote"),
    )