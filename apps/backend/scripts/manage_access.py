import argparse
import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domains.access.models import AccessCode
from app.utils.security import hash_access_code

def add_code(code: str):
    db: Session = SessionLocal()
    try:
        hashed = hash_access_code(code)
        exists = db.query(AccessCode).filter(AccessCode.code == hashed).first()
        if exists:
            print(f"Code already exists (ID: {exists.id}). Active: {exists.is_active}")
            return
        
        new_code = AccessCode(code=hashed, is_active=True)
        db.add(new_code)
        db.commit()
        print(f"Successfully added new access code. ID: {new_code.id}")
    except Exception as e:
        print(f"Error adding code: {e}")
    finally:
        db.close()

def list_codes():
    db: Session = SessionLocal()
    try:
        codes = db.query(AccessCode).all()
        print(f"{'ID':<5} | {'Active':<8} | {'Created At':<25} | {'Hash (Prefix)'}")
        print("-" * 60)
        for c in codes:
            print(f"{c.id:<5} | {str(c.is_active):<8} | {str(c.created_at):<25} | {c.code[:10]}...")
    finally:
        db.close()

def set_status(code_id: int, active: bool):
    db: Session = SessionLocal()
    try:
        code = db.query(AccessCode).filter(AccessCode.id == code_id).first()
        if not code:
            print(f"Code with ID {code_id} not found.")
            return
        
        code.is_active = active
        db.commit()
        status = "Active" if active else "Disabled"
        print(f"Code ID {code_id} is now {status}.")
    except Exception as e:
        print(f"Error updating status: {e}")
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Manage Access Codes")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new access code")
    add_parser.add_argument("code", type=str, help="The plain text access code to add")

    # List command
    subparsers.add_parser("list", help="List all access codes")

    # Revoke command
    revoke_parser = subparsers.add_parser("revoke", help="Disable an access code by ID")
    revoke_parser.add_argument("id", type=int, help="ID of the code to disable")

    # Enable command
    enable_parser = subparsers.add_parser("enable", help="Enable an access code by ID")
    enable_parser.add_argument("id", type=int, help="ID of the code to enable")

    args = parser.parse_args()

    if args.command == "add":
        add_code(args.code)
    elif args.command == "list":
        list_codes()
    elif args.command == "revoke":
        set_status(args.id, False)
    elif args.command == "enable":
        set_status(args.id, True)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
