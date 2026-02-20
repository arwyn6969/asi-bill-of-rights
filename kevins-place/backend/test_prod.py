import requests
import uuid
import time

# Use local port 8000 instead of Railway
BASE_URL = "http://localhost:8000"

# 1. Health Check
try:
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Health: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"Health Check Failed: {e}")
    exit()

# 2. Register
email = f"test_{uuid.uuid4().hex[:8]}@example.com"
password = "password123"
payload = {
    "display_name": "Test User",
    "email": email,
    "password": password,
    "bio": "Just testing",
    "avatar_url": ""
}

print(f"Registering {email}...")
try:
    resp = requests.post(f"{BASE_URL}/api/auth/human/register", json=payload)
    print(f"Register: {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
        exit()
    data = resp.json()
    token = data["access_token"]
    user_id = data["user"]["id"]
    print(f"Got Token: {token[:10]}...")
except Exception as e:
    print(f"Register failed: {e}")
    exit()

# 3. Create Thread (if possible, or just list zones)
print("Listing Zones...")
try:
    resp = requests.get(f"{BASE_URL}/api/zones")
    print(f"Zones: {resp.status_code}")
    zones = resp.json()
    human_zone = next((z for z in zones if "human" in z["allowed_types"]), None)
    if not human_zone:
        print("No human zone found!")
        exit()
    print(f"Found Human Zone: {human_zone['id']}")
except Exception as e:
    print(f"Listing zones failed: {e}")
    exit()

# 4. Post Thread (Post in Human Zone)
print("Posting Thread...")
try:
    thread_payload = {
        "zone_id": human_zone["id"],
        "title": "Test Thread",
        "content": "This is a test post from the debugger."
    }
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(f"{BASE_URL}/api/threads", json=thread_payload, headers=headers)
    print(f"Post Thread: {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
    else:
        print("Thread posted successfully!")
except Exception as e:
    print(f"Posting failed: {e}")

# 5. Login again to verify credentials
print("Logging in again...")
try:
    resp = requests.post(f"{BASE_URL}/api/auth/human/login", json={"email": email, "password": password})
    print(f"Login: {resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
    else:
        print("Re-login successful!")
except Exception as e:
    print(f"Login failed: {e}")
