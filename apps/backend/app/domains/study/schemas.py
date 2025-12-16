from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: Optional[str] = None # frontend uses role
    sender: Optional[str] = None # backend uses sender
    content: str

class StudyChatRequest(BaseModel):
    # Legacy / compatible with old frontend for now
    history: List[Message] = []
    message: str
    language: str = "english"
    session_id: Optional[str] = None
    subject_id: Optional[str] = None 

class StudyChatResponse(BaseModel):
    answer: str
    session_id: Optional[str] = None

class StudyExplainRequest(BaseModel):
    topic: str
    language: str
    context: Optional[str] = None
    subject_id: Optional[str] = None # Required for new flow, optional for legacy transition

class StudyExplainResponse(BaseModel):
    explanation: str
    session_id: str
    slug: Optional[str] = None
    topic_id: Optional[str] = None

# New Multipage Schemas
class CreateTopicRequest(BaseModel):
    subject_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    language: str = "english"
    context: Optional[str] = None

class TopicResponse(BaseModel):
    id: str
    slug: str
    title: str
    description: Optional[str] = None
    content: str
    subject_id: str
    is_featured: bool
    language: str = "english"

class StartChatRequest(BaseModel):
    topic_id: str
    topic_name: Optional[str] = None
    initial_context: Optional[str] = None
    language: str = "english"

class ChatSessionResponse(BaseModel):
    session_id: str
    topic_id: str

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "english"

class ChatResponse(BaseModel):
    answer: str
    session_id: str
