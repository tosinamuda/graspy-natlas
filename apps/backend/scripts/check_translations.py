import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.domains.study.models import Topic, TopicTranslation
from app.domains.subject.models import Subject

def check_translations(topic_id: str):
    db = SessionLocal()
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
             print(f"Topic {topic_id} not found.")
             return

        print(f"Checking Topic: {topic.title} ({topic.id}) Slug: {topic.slug}")
        
        translations = db.query(TopicTranslation).filter(TopicTranslation.topic_id == topic.id).all()
        if not translations:
            print("  No translations found.")
        else:
            for t in translations:
                # Print more content to detect language
                content_preview = t.content[:100].replace("\n", " ") if t.content else "None"
                print(f"  - Lang: {t.language}, Content: {content_preview}...")

    except Exception as e:
        print(f"Error checking translations: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_translations("e45dcc83-6f9a-4106-b493-bc425d7ee80e")
