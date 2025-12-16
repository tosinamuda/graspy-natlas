from sqlalchemy.orm import Session
from app.domains.study.models import InteractionLog, User, Topic, ChatSession, ChatMessage
from typing import Optional, List
import json

class StudyRepository:
    """
    Legacy repository for InteractionLog
    """
    @staticmethod
    def create_log(
        db: Session,
        interaction_type: str,
        user_input: str,
        ai_response: str,
        topic: str = None,
        language: str = "english",
        context: dict = None,
        session_id: str = None
    ) -> InteractionLog:
        """
        Create a new interaction log entry.
        """
        log_entry = InteractionLog(
            interaction_type=interaction_type,
            user_input=user_input,
            ai_response=ai_response,
            topic=topic,
            language=language,
            context=json.dumps(context) if context else None,
            session_id=session_id
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry

    @staticmethod
    def get_logs_by_session(db: Session, session_id: str):
        """
        Retrieve all interaction logs for a specific session, ordered by time.
        """
        return db.query(InteractionLog).filter(
            InteractionLog.session_id == session_id
        ).order_by(InteractionLog.id.asc()).all()

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        return self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
        
    def create(self, email: str, firebase_uid: str) -> User:
        user = User(email=email, firebase_uid=firebase_uid)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
        
    def verify_access(self, user: User):
        user.is_verified = True
        self.db.commit()
        self.db.refresh(user)

class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, slug: str, subject_id: str, content: str = None, description: str = None, user_id: str = None, is_featured: bool = False, is_public: bool = False, language: str = "english") -> Topic:
        topic = Topic(
            title=title, slug=slug, subject_id=subject_id,
            content=content, description=description, created_by_user_id=user_id,
            is_featured=is_featured, is_public=is_public,
            language=language
        )
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def get_by_id(self, id: str) -> Optional[Topic]:
        return self.db.query(Topic).filter(Topic.id == id).first()

    def get_by_slug_and_subject(self, slug: str, subject_id: str) -> Optional[Topic]:
        return self.db.query(Topic).filter(Topic.slug == slug, Topic.subject_id == subject_id).first()

    def list_by_subject(self, subject_id: str, is_public_only: bool = True) -> List[Topic]:
        q = self.db.query(Topic).filter(Topic.subject_id == subject_id)
        if is_public_only:
            q = q.filter(Topic.is_public == True)
        return q.all()
        
    def list_featured(self) -> List[Topic]:
        return self.db.query(Topic).filter(Topic.is_featured == True, Topic.is_public == True).all()

    def get_translation(self, topic_id: str, language: str):
        # Local import to avoid circular dependency if models imported at top
        from app.domains.study.models import TopicTranslation
        return self.db.query(TopicTranslation).filter(
            TopicTranslation.topic_id == topic_id,
            TopicTranslation.language == language
        ).first()

    def add_translation(self, topic_id: str, language: str, content: str):
        from app.domains.study.models import TopicTranslation
        translation = TopicTranslation(
            topic_id=topic_id,
            language=language,
            content=content
        )
        self.db.add(translation)
        self.db.commit()
        self.db.refresh(translation)
        return translation

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: str, topic_id: str) -> ChatSession:
        session = ChatSession(user_id=user_id, topic_id=topic_id)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
        
    def get_session(self, session_id: str) -> Optional[ChatSession]:
         return self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    def get_session_by_user_and_topic(self, user_id: str, topic_id: str) -> Optional[ChatSession]:
        return self.db.query(ChatSession).filter(ChatSession.user_id == user_id, ChatSession.topic_id == topic_id).order_by(ChatSession.created_at.desc()).first()

    def add_message(self, session_id: str, role: str, content: str) -> ChatMessage:
        msg = ChatMessage(session_id=session_id, role=role, content=content)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_history(self, session_id: str) -> List[ChatMessage]:
        return self.db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
