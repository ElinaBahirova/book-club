import requests
import sys

DEPLOYED_URL = "https://book-club-backend-j2lp.onrender.com/api/health"

def check_deployment():
    print(f"--- Verifying Deployment at {DEPLOYED_URL} ---")
    try:
        response = requests.get(DEPLOYED_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: {data['message']}")
            print(f"📊 Status: {data['status']} | DB: {data['database']}")
        else:
            print(f"❌ FAILED: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"🚫 ERROR: Could not reach the server. {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_deployment()