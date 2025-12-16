from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.domains.study.service import StudyService
from app.domains.auth import get_current_verified_user
from app.domains.study.models import User
from app.domains.study.schemas import (
    StudyChatRequest, StudyChatResponse, 
    StudyExplainRequest, StudyExplainResponse, 
    CreateTopicRequest, TopicResponse, ChatRequest, ChatResponse,
    StartChatRequest, ChatSessionResponse
)

router = APIRouter(prefix="/study", tags=["Study"])

@router.post("/topics", response_model=TopicResponse)
async def create_topic(
    payload: CreateTopicRequest, 
    user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    service = StudyService(db)
    try:
        subject_id = payload.subject_id
        if not subject_id:
             # Fallback to 'uncategorized'
            uncategorized = service.subject_repo.get_by_slug("uncategorized")
            if not uncategorized:
                 # Should exist from seed, but handle just in case
                uncategorized = service.subject_repo.create("Uncategorized", "uncategorized", is_featured=True)
            subject_id = uncategorized.id

        topic = await service.get_or_create_topic(
            subject_id=subject_id,
            title=payload.title,
            user=user,
            language=payload.language,
            context_instruction=payload.context,
            description=payload.description
        )
        return topic
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics/stream")
async def stream_create_topic(
    topic: str,
    subject_id: str = None,
    language: str = "english",
    context: str = None,
    user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    SSE Endpoint for streaming topic creation.
    """
    service = StudyService(db)
    
    # Handle Default Subject Logic (Duplicate from Create but needed here)
    if not subject_id:
        uncategorized = service.subject_repo.get_by_slug("uncategorized")
        if not uncategorized:
            uncategorized = service.subject_repo.create("Uncategorized", "uncategorized", is_featured=True)
        subject_id = uncategorized.id

    return StreamingResponse(
        service.create_topic_generator(
            subject_id=subject_id,
            title=topic,
            user=user,
            language=language,
            context_instruction=context
        ),
        media_type="text/event-stream"
    )

@router.get("/topics/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: str,
    language: str = "english",
    db: Session = Depends(get_db)
):
    service = StudyService(db)
    topic = await service.get_topic_by_id(topic_id, language=language)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/chat/start", response_model=ChatSessionResponse)
async def start_chat(
    payload: StartChatRequest,
    user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    service = StudyService(db)
    try:
        session = await service.start_chat_session(
            user=user, 
            topic_id=payload.topic_id,
            topic_name=payload.topic_name,
            initial_context=payload.initial_context,
            language=payload.language
        )
        return ChatSessionResponse(session_id=session.id, topic_id=session.topic_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def study_chat(
    payload: ChatRequest, 
    user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    service = StudyService(db)
    try:
        result = await service.chat(
            session_id=payload.session_id,
            message=payload.message,
            language=payload.language,
            user=user
        )
        return ChatResponse(**result)
    except ValueError as ve:
        raise HTTPException(status_code=403, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain", response_model=StudyExplainResponse)
async def study_explain(
    payload: StudyExplainRequest, 
    user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Legacy/Hybrid endpoint: generates explanation (Topic) and returns it with a new Session ID.
    """
    service = StudyService(db)
    try:
        subject_id = payload.subject_id
        if not subject_id:
            # Fallback to 'uncategorized' subject
            uncategorized = service.subject_repo.get_by_slug("uncategorized")
            if not uncategorized:
                uncategorized = service.subject_repo.create("Uncategorized", "uncategorized", is_featured=True)
            subject_id = uncategorized.id

        topic = await service.get_or_create_topic(
            subject_id=subject_id,
            title=payload.topic,
            user=user,
            language=payload.language,
            context_instruction=payload.context
        )
        
        # Start a new chat session for this topic
        session = await service.start_chat_session(user, topic.id)
        
        return StudyExplainResponse(
            explanation=topic.content,
            session_id=session.id,
            slug=topic.slug,
            topic_id=topic.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
