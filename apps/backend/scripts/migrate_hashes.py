import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domains.access.models import AccessCode
from app.utils.security import hash_access_code

def migrate_to_hash():
    db: Session = SessionLocal()
    try:
        # 1. Identify codes that are NOT sha-256 length (64 chars hex)
        # Note: Access codes are user defined, but standard passwords are usually shorter.
        # SHA256 hex digest is exactly 64 chars.
        
        all_codes = db.query(AccessCode).all()
        migrated_count = 0
        
        for entry in all_codes:
            if len(entry.code) != 64:
                print(f"Migrating plain text code: {entry.code}")
                # Hash it
                entry.code = hash_access_code(entry.code)
                migrated_count += 1
        
        if migrated_count > 0:
            db.commit()
            print(f"Successfully migrated {migrated_count} access codes to SHA-256.")
        else:
            print("No plain text codes found (or all matched hash length).")
            
    except Exception as e:
        print(f"Error migrating DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_to_hash()
