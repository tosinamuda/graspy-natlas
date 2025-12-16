from app.database import SessionLocal
from app.database import SessionLocal
from app.domains.study.models import Topic
# Import Subject to ensure registry is populated
import app.domains.subject.models

db = SessionLocal()
topic_id = "73a608ce-16ff-4122-8ebc-4e83b61374b0"
topic = db.query(Topic).filter(Topic.id == topic_id).first()
if topic:
    # Manually delete translations first because cascade is missing in model
    for trans in topic.translations:
        db.delete(trans)
    
    db.delete(topic)
    db.commit()
else:
    print("Topic not found")
