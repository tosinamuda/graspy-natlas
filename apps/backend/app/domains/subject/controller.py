from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.domains.subject.service import SubjectService
from app.domains.subject.schemas import SubjectListResponse, SubjectSchema

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("", response_model=SubjectListResponse)
def list_subjects(
    featured: bool = Query(False, description="Filter by featured subjects"),
    db: Session = Depends(get_db)
):
    service = SubjectService(db)
    subjects = service.list_subjects(featured_only=featured)
    return SubjectListResponse(subjects=subjects)

@router.get("/{slug}", response_model=SubjectSchema)
def get_subject(slug: str, db: Session = Depends(get_db)):
    service = SubjectService(db)
    subject = service.get_subject_by_slug(slug)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject
