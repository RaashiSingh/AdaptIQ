from sqlalchemy import Column, String, DateTime, Float, JSON, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.db import Base

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    quiz_score = Column(Float, nullable=True)
    weak_areas = Column(JSON, default=[])
    messages = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())