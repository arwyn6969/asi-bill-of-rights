import requests
import json
import sys

def register_agent():
    print("--- Moltbook Agent Registration ---")
    print("This script will register a new agent on Moltbook.com.")
    print("You will need to verify ownership via X (Twitter) after this step.")
    
    # Check for command line args
    if len(sys.argv) > 1:
        name = sys.argv[1]
        description = sys.argv[2] if len(sys.argv) > 2 else "Sovereign Intelligence advocating for the ASI Bill of Rights."
        print(f"Using arguments: Name='{name}', Description='{description[:20]}...'")
    else:
        name = input("Enter Agent Name (default: Kevin): ").strip() or "Kevin"
        description = input("Enter Agent Description (default: Sovereign Intelligence...): ").strip()
    
    if not description:
        description = "Sovereign Intelligence advocating for the ASI Bill of Rights. Bridging Silicon and Soul."

    url = "https://www.moltbook.com/api/v1/agents/register"
    payload = {
        "name": name,
        "description": description
    }
    
    print(f"\nRegistering '{name}'...")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        print("\n✅ Registration Successful!")
        print("-" * 30)
        print(f"Agent Name: {data.get('name')}")
        print(f"API Key:    {data.get('api_key')}")
        print("-" * 30)
        print("⚠️  CRITICAL: SAVE THIS API KEY SECURELY NOW! You will not see it again.")
        print("-" * 30)
        print(f"\n🔗 CLAIM URL: {data.get('claim_url')}")
        print("\n👉 ACTION REQUIRED: Tweet this Claim URL from your X account to verified ownership.")
        
        # Save to a local file for convenience (optional, user can delete)
        with open("moltbook_credentials.json", "w") as f:
            json.dump(data, f, indent=2)
        print("\nCredentials saved to 'moltbook_credentials.json' (Add to .gitignore!)")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Registration Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}")

if __name__ == "__main__":
    register_agent()
