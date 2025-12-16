from app.database import SessionLocal
from app.domains.study.models import Topic, TopicTranslation
import app.domains.subject.models # Verify registry

db = SessionLocal()
topics = db.query(Topic).all()

count = 0
for topic in topics:
    if not topic.content:
        continue
        
    # Check if translation exists for this language
    exists = db.query(TopicTranslation).filter(
        TopicTranslation.topic_id == topic.id,
        TopicTranslation.language == topic.language
    ).first()
    
    if not exists:
        print(f"Migrating {topic.title} ({topic.language})...")
        trans = TopicTranslation(
            topic_id=topic.id,
            language=topic.language,
            content=topic.content
        )
        db.add(trans)
        count += 1

db.commit()
print(f"Migration complete. Moved {count} topics to translations.")
