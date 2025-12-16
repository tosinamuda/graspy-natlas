from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.base import Base

class AccessCode(Base):
    __tablename__ = "access_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
