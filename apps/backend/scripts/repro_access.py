import requests
import sys
import os

# Add parent directory to path to allow importing app (if needed in future)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8082/api"

def repro_issue():
    print("Repro: Testing lowercase 'tosin'...")
    try:
        # Lowercase "tosin" should fail currently if case sensitive
        # But we want it to PASS after fix. 
        # So initially this script will fail (return False) if the API returns invalid.
        
        res = requests.post(f"{BASE_URL}/access/verify", json={"code": "tosin"})
        data = res.json()
        
        print(f"Response: {res.status_code} {res.text}")
        
        if res.ok and data.get("valid"):
            print("PASS: Access code 'tosin' accepted.")
            return True
        else:
            print("FAIL: Access code 'tosin' rejected.")
            return False
            
    except Exception as e:
        print(f"Error validating: {e}")
        return False

if __name__ == "__main__":
    if repro_issue():
        sys.exit(0)
    else:
        sys.exit(1)
