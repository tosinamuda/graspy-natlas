import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domains.study.models import Topic, TopicTranslation, ChatSession, ChatMessage, InteractionLog
from app.domains.subject.models import Subject

def delete_topic(topic_id: str):
    db: Session = SessionLocal()
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            print(f"Topic {topic_id} not found.")
            return

        print(f"Found Topic: {topic.title} ({topic.id})")

        # 1. Find related Sessions
        sessions = db.query(ChatSession).filter(ChatSession.topic_id == topic_id).all()
        session_ids = [s.id for s in sessions]
        print(f"Found {len(sessions)} chat sessions.")

        # 2. Delete Chat Messages
        if session_ids:
            deleted_msgs = db.query(ChatMessage).filter(ChatMessage.session_id.in_(session_ids)).delete(synchronize_session=False)
            print(f"Deleted {deleted_msgs} chat messages.")
            
            # 3. Delete Interaction Logs linked to these sessions
            deleted_logs = db.query(InteractionLog).filter(InteractionLog.session_id.in_(session_ids)).delete(synchronize_session=False)
            print(f"Deleted {deleted_logs} interaction logs.")

        # 4. Delete Sessions
        deleted_sessions = db.query(ChatSession).filter(ChatSession.topic_id == topic_id).delete(synchronize_session=False)
        print(f"Deleted {deleted_sessions} chat sessions.")

        # 5. Delete Translations
        deleted_translations = db.query(TopicTranslation).filter(TopicTranslation.topic_id == topic_id).delete(synchronize_session=False)
        print(f"Deleted {deleted_translations} translations.")

        # 6. Delete Topic
        db.delete(topic)
        db.commit()
        print(f"Successfully deleted topic {topic.id} and all related data.")

    except Exception as e:
        print(f"Error deleting topic: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_topic.py <topic_id>")
        sys.exit(1)
    
    target_id = sys.argv[1]
    delete_topic(target_id)
