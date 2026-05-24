from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.base import Base

question_tags = Table(
    "question_tags",
    Base.metadata,
    Column("question_id", UUID(as_uuid=True), ForeignKey("questions.id"), primary_key=True, nullable=False),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True, nullable=False),
)