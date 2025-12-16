from sqlalchemy.orm import Session
from app.domains.subject.repository import SubjectRepository
from app.domains.subject.models import Subject
from typing import List, Optional

class SubjectService:
    def __init__(self, db: Session):
        self.repo = SubjectRepository(db)

    def list_subjects(self, featured_only: bool = False) -> List[Subject]:
        return self.repo.list_all(featured_only=featured_only)

    def get_subject_by_slug(self, slug: str) -> Optional[Subject]:
        return self.repo.get_by_slug(slug)
    
    def create_subject(self, name: str, slug: str, is_featured: bool = False) -> Subject:
        # TODO: checking slug uniqueness?
        existing = self.repo.get_by_slug(slug)
        if existing:
             # handle simple slug collision or raise?
             # For now, simple fail or assumes unique input
             pass
        return self.repo.create(name, slug, is_featured)
