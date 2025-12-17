from sqlalchemy.orm import Session
from app.domains.access.models import AccessCode
from app.utils.security import hash_access_code

class AccessRepository:
    @staticmethod
    def get_active_code(db: Session, code: str) -> AccessCode:
        # Normalize: trim and uppercase to handle user input variations
        normalized_code = code.strip().upper()
        hashed_code = hash_access_code(normalized_code)
        return db.query(AccessCode).filter(
            AccessCode.code == hashed_code,
            AccessCode.is_active == True
        ).first()
