import requests
import json
import time

BASE_URL = "http://localhost:8082/api/study"
HEADERS = {"Content-Type": "application/json", "x-access-code": "TEST_PIDGIN"}

def test_chat():
    print("1. Explaining Electrolysis...")
    try:
        resp = requests.post(f"{BASE_URL}/explain", json={"topic": "Electrolysis", "language": "english", "context": "Explain briefly."}, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        session_id = data.get("session_id")
        print(f"Session ID: {session_id}")
        explanation = data.get('explanation')
        print(f"Explanation: {explanation[:50]}...")
    except Exception as e:
        print(f"Error in step 1: {e}")
        if 'resp' in locals():
            print(f"Response: {resp.text}")
        return

    print("\n2. User: What are the relevant formulae?")
    resp = requests.post(f"{BASE_URL}/chat", json={"message": "What are the relevant formulae?", "session_id": session_id, "language": "english", "history": []}, headers=HEADERS)
    print(f"AI: {resp.json().get('answer')}")

    print("\n3. User: Show me the equations.")
    resp = requests.post(f"{BASE_URL}/chat", json={"message": "Show me the equations.", "session_id": session_id, "language": "english", "history": []}, headers=HEADERS)
    print(f"AI: {resp.json().get('answer')}")

    print("4. User: Where is the equation?")
    resp = requests.post(f"{BASE_URL}/chat", json={"message": "Where is the equation?", "session_id": session_id, "language": "english", "history": []}, headers=HEADERS)
    print(f"AI: {resp.json().get('answer')}")

if __name__ == "__main__":
    test_chat()
