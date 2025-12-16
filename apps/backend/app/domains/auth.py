from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.domains.study.repository import UserRepository
from app.domains.study.models import User
from app.settings import get_settings
import os
import json

security = HTTPBearer()
settings = get_settings()

def get_firebase_app():
    try:
        if not firebase_admin._apps:
            # 1. Check for file path first (User preference)
            if settings.firebase_credentials_path and os.path.exists(settings.firebase_credentials_path):
                 cred = credentials.Certificate(settings.firebase_credentials_path)
                 firebase_admin.initialize_app(cred)
            # 2. Check for raw JSON content
            elif settings.firebase_service_account_json:
                cred = credentials.Certificate(json.loads(settings.firebase_service_account_json))
                firebase_admin.initialize_app(cred)
            else:
                 # 3. Fallback to default google credentials search
                firebase_admin.initialize_app()
        return firebase_admin.get_app()
    except ValueError:
        # App already exists
        return firebase_admin.get_app()

# Initialize on module load if possible, or lazy load in dependency
# Lazy loading is safer for tests/environments without creds immediately available
get_firebase_app()

def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = cred.credentials
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token.get('email', '')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_firebase_uid(uid)
    
    if not user:
        # On-the-fly user creation
        user = user_repo.create(email=email, firebase_uid=uid)
        
    return user

def get_current_verified_user(
    user: User = Depends(get_current_user)
) -> User:
    """
    Ensures user has entered a valid access code at least once.
    """
    settings = get_settings()
    if not settings.enable_access_control:
        return user
        
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access code verification required. Please activate your account."
        )
    return user
