import asyncio
import sys
import os
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.domains.study.service import StudyService
from app.domains.study.repository import StudyRepository

async def verify():
    db = SessionLocal()
    service = StudyService(db)
    
    session_id = str(uuid.uuid4())
    print(f"Testing Backend Retrieval & Compaction. Session ID: {session_id}")
    
    # 1. Seed History in DB (Explanation + 4 Chat Turns) -> 10 messages total
    # Explanation
    StudyRepository.create_log(db, "explanation", "Photosynthesis", "Photosynthesis is the process by which plants make food using sunlight.", topic="Photosynthesis", session_id=session_id)
    
    # Chat Turns (4 turns = 8 messages)
    chat_turns = [
        ("What are the inputs?", "The inputs are carbon dioxide, water, and sunlight."),
        ("What are the outputs?", "The outputs are glucose (sugar) and oxygen."),
        ("Where does it happen?", "It happens in the chloroplasts."),
        ("What is the pigment called?", "The pigment is chlorophyll.")
    ]
    
    for q, a in chat_turns:
        StudyRepository.create_log(db, "chat", q, a, session_id=session_id)
            
    print("Seeded database with history (10 messages).")
    
    # 2. Call Chat with EMPTY Frontend History
    # This proves the backend is fetching from the DB
    print("Calling Service with EMPTY history payload...")
    response = await service.chat(
        history=[], # EMPTY!
        message="Why is it green?",
        language="English",
        session_id=session_id
    )
    
    print("\n--- Response ---")
    print(response["answer"])
    print("\n--- Verification Check ---")
    print("Look for logs above:")
    print("1. 'Reconstructing history from 10 logs...'")
    print("2. 'Compacting history...'")

if __name__ == "__main__":
    asyncio.run(verify())
