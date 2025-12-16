from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from .models import Subject

class SubjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, slug: str, is_featured: bool = False) -> Subject:
        subject = Subject(name=name, slug=slug, is_featured=is_featured)
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject

    def get_by_slug(self, slug: str) -> Optional[Subject]:
        return self.db.query(Subject).options(joinedload(Subject.topics)).filter(Subject.slug == slug).first()

    def get_by_id(self, id: str) -> Optional[Subject]:
        return self.db.query(Subject).options(joinedload(Subject.topics)).filter(Subject.id == id).first()

    def list_all(self, featured_only: bool = False) -> List[Subject]:
        q = self.db.query(Subject).options(joinedload(Subject.topics))
        if featured_only:
            q = q.filter(Subject.is_featured == True)
        return q.all()
