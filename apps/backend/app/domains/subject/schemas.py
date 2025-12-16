from pydantic import BaseModel
from typing import List, Optional

class TopicSummarySchema(BaseModel):
    id: str
    title: str
    slug: str
    description: Optional[str] = None
    is_featured: bool

    class Config:
        from_attributes = True

class SubjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    is_featured: bool
    topics: List[TopicSummarySchema] = []

    class Config:
        from_attributes = True

class SubjectListResponse(BaseModel):
    subjects: List[SubjectSchema]
