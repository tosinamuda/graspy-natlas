from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.settings import get_settings
from app.domains.access.repository import AccessRepository

def verify_access_code(
    x_access_code: str = Header(None, alias="x-access-code"),
    db: Session = Depends(get_db)
):
    """
    Dependency to verify x-access-code header.
    Skipped if ENABLE_ACCESS_CONTROL is False.
    """
    settings = get_settings()
    
    if not settings.enable_access_control:
        return True

    if not x_access_code:
        raise HTTPException(status_code=401, detail="Access code required")

    code_entry = AccessRepository.get_active_code(db, x_access_code)
    if not code_entry:
        raise HTTPException(status_code=401, detail="Invalid access code")
        
    return True
