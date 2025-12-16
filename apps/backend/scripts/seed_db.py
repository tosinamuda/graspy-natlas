import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domains.access.models import AccessCode

def seed():
    # Load settings to check config
    from app.settings import get_settings
    settings = get_settings()
    
    code_str = settings.initial_access_code

    if not code_str:
        if settings.enable_access_control:
            raise ValueError("CRITICAL: INITIAL_ACCESS_CODE must be set when ENABLE_ACCESS_CONTROL is True.")
        else:
            print("Access control disabled and no code provided. Skipping seed.")
            return

    db: Session = SessionLocal()
    from app.utils.security import hash_access_code
    try:
        hashed_code = hash_access_code(code_str)
        exists = db.query(AccessCode).filter(AccessCode.code == hashed_code).first()
        if not exists:
            new_code = AccessCode(code=hashed_code, is_active=True)
            db.add(new_code)
            db.commit()
            print(f"Seeded hashed access code for: {code_str}...")
        else:
            print(f"Access code already exists (hashed).")
            
    except Exception as e:
        print(f"Error seeding DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
