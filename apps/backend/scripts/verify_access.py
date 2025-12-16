import requests
import sys
import os

# Add parent directory to path to allow importing app (if needed in future)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8082/api"

def verify_access_control():
    # 1. Try without code (Should fail)
    try:
        res = requests.post(f"{BASE_URL}/study/chat", json={"message": "test", "language": "english"})
        if res.status_code != 401:
            print(f"FAIL: Expected 401 without code, got {res.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting: {e}")
        return False
        
    print("PASS: Access denied without code.")

    # 2. Verify code endpoint
    try:
        res = requests.post(f"{BASE_URL}/access/verify", json={"code": "TOSIN"})
        if not res.ok or not res.json().get("valid"):
            print(f"FAIL: Verification failed for valid code. {res.text}")
            return False
    except Exception as e:
        print(f"Error verifying: {e}")
        return False
        
    print("PASS: Code verification succeeded.")

    # 3. Try with code
    try:
        res = requests.post(
            f"{BASE_URL}/study/chat", 
            json={"message": "MOCK_TEST", "language": "english"},
            headers={"x-access-code": "TOSIN"}
        )
        # Note: MOCK_TEST might not work if I reverted logic, but 200 OK is enough to prove access
        if res.status_code != 200:
             print(f"FAIL: Expected 200 with code, got {res.status_code}. Body: {res.text}")
             return False
    except Exception as e:
        print(f"Error chat with code: {e}")
        return False
        
    print("PASS: Access granted with valid code.")
    return True

if __name__ == "__main__":
    if verify_access_control():
        sys.exit(0)
    else:
        sys.exit(1)
