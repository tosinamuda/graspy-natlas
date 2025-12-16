from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.domains.access.schemas import VerifyAccessRequest, VerifyAccessResponse
from app.domains.access.repository import AccessRepository
from app.domains.study.repository import UserRepository
from app.domains.auth import get_current_user
from app.domains.study.models import User
from app.settings import get_settings

router = APIRouter(prefix="/access", tags=["Access"])

@router.post("/verify", response_model=VerifyAccessResponse)
async def verify_code(payload: VerifyAccessRequest, db: Session = Depends(get_db)):
    """
    Check if a code is valid (Stateless check).
    """
    settings = get_settings()
    if not settings.enable_access_control:
        return VerifyAccessResponse(valid=True)
    
    code_entry = AccessRepository.get_active_code(db, payload.code)
    if not code_entry:
        raise HTTPException(status_code=401, detail="Invalid access code")
        
    return VerifyAccessResponse(valid=True)

@router.post("/activate", response_model=VerifyAccessResponse)
async def activate_access(
    payload: VerifyAccessRequest, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activate the current user's account with an access code.
    """
    settings = get_settings()
    if not settings.enable_access_control:
        return VerifyAccessResponse(valid=True)
        
    code_entry = AccessRepository.get_active_code(db, payload.code)
    if not code_entry:
        raise HTTPException(status_code=401, detail="Invalid access code")
    
    try:
        user_repo = UserRepository(db)
        user_repo.verify_access(user)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Failed to activate user: {e}")
    
    return VerifyAccessResponse(valid=True)

@router.get("/status")
async def check_access_status(
    user: User = Depends(get_current_user),
):
    """
    Check if the current user is verified.
    """
    return {"is_verified": user.is_verified}
