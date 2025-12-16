from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    is_featured = Column(Boolean, default=False)

    topics = relationship("app.domains.study.models.Topic", back_populates="subject")
