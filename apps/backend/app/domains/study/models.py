from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.base import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False) # True if access code entered
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("subjects.id"), nullable=False)
    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True) 
    
    title = Column(String, nullable=False)
    slug = Column(String, index=True, nullable=False) 
    description = Column(String, nullable=True)
    content = Column(Text, nullable=True) # Initial explanation
    language = Column(String, default="english", nullable=False) # Language of the 'content'
    
    is_featured = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    subject = relationship("app.domains.subject.models.Subject", back_populates="topics")
    translations = relationship("TopicTranslation", back_populates="topic", cascade="all, delete-orphan")

class TopicTranslation(Base):
    __tablename__ = "topic_translations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_id = Column(String, ForeignKey("topics.id"), nullable=False)
    language = Column(String, nullable=False) # e.g. 'yoruba', 'hausa'
    content = Column(Text, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    topic = relationship("Topic", back_populates="translations")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_id = Column(String, ForeignKey("topics.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    messages = relationship("ChatMessage", back_populates="session")
    topic = relationship("Topic")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False) # user/assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("ChatSession", back_populates="messages")

class InteractionLog(Base):
    """
    SQLAlchemy model for logging study interactions.
    """
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    interaction_type = Column(String, index=True) # 'chat' or 'explanation'
    topic = Column(String, index=True, nullable=True) # Topic being discussed/explained
    language = Column(String) # Language used
    user_input = Column(Text) # The question or topic prompt
    ai_response = Column(Text) # The generated answer/explanation
    context = Column(Text, nullable=True) # JSON string or text dump of history/context
    session_id = Column(String, index=True, nullable=True) # Linking interactions to a session
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
