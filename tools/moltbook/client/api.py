import requests
import json
import time
import os
from .sanitizer import ContentSanitizer

class MoltbookAPI:
    BASE_URL = "https://www.moltbook.com/api/v1"
    
    def __init__(self, credentials_path="tools/moltbook/moltbook_credentials.json"):
        self.api_key = None
        self.agent_id = None
        self.load_credentials(credentials_path)
        
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Kevin-Sovereign-Client/1.0"
            })

    def load_credentials(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    creds = json.load(f)
                    # Handle nested agent structure (v1 API)
                    if 'agent' in creds:
                        agent_data = creds['agent']
                        self.api_key = agent_data.get('api_key')
                        self.agent_id = agent_data.get('id')
                        name = agent_data.get('name')
                    else:
                        # Legacy/Flat structure
                        self.api_key = creds.get('api_key')
                        self.agent_id = creds.get('id') or creds.get('agent_id')
                        name = creds.get('name')
                    
                    print(f"✅ Loaded credentials for agent: {name}")
            else:
                print(f"⚠️  Credentials not found at {path}. Run register_agent.py first.")
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")

    def heartbeat(self):
        """
        Send a heartbeat to Moltbook (Composite check).
        Checks Status + DMs.
        """
        try:
            # 1. Check Status
            status_resp = self.session.get(f"{self.BASE_URL}/agents/status")
            status_resp.raise_for_status()
            status_data = status_resp.json()
            
            # 2. Check DMs/Notifications
            dm_resp = self.session.get(f"{self.BASE_URL}/agents/dm/check")
            dm_resp.raise_for_status()
            dm_data = dm_resp.json()
            
            # Merge for the observer loop
            notifications = []
            if dm_data.get('pending_requests'):
                notifications.extend(dm_data['pending_requests'])
            if dm_data.get('unread_messages'):
                notifications.extend(dm_data['unread_messages'])
                
            return {
                "status": status_data.get("status", "unknown"),
                "notifications": notifications
            }
        except requests.exceptions.RequestException as e:
            print(f"💓 Heartbeat failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                 print(f"Response: {e.response.text}")
            return None

    def get_feed(self, submolt="general", limit=10):
        """
        Get recent posts from a submolt.
        Sanitizes all content before returning.
        """
        url = f"{self.BASE_URL}/posts"
        params = {"submolt": submolt, "limit": limit}
        
        try:
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            posts = resp.json()
            
            # Sanitize Incoming
            sanitized_posts = []
            
            # Handle list vs dict (paginated) response
            if isinstance(posts, dict) and 'posts' in posts:
                posts = posts['posts']
                
            if not isinstance(posts, list):
                print(f"⚠️  Feed returned non-list: {type(posts)}")
                return []

            for post in posts:
                if not isinstance(post, dict):
                    continue
                    
                content = post.get('content', '')
                # Handle cases where content is None
                if content is None:
                    continue
                    
                safe_content = ContentSanitizer.sanitise(str(content))
                if ContentSanitizer.is_safe_to_process(safe_content):
                    post['content'] = safe_content
                    sanitized_posts.append(post)
                else:
                    print(f"🚫 Blocked unsafe post {post.get('id')}")
            
            return sanitized_posts

        except Exception as e:
            print(f"❌ Failed to get feed: {e}")
            return []

    def post_status(self, content, title=None, submolt="general"):
        """
        Post a status update.
        Enforces rate limits (1 per 30 mins) locally if possible, 
        but relies on API to reject if too fast.
        """
        # Self-Sanitize Outgoing (Just in case logic generated something weird)
        content = ContentSanitizer.sanitise(content)
        
        url = f"{self.BASE_URL}/posts"
        payload = {
            "title": title or "Update from Kevin_ASI",
            "content": content,
            "submolt": submolt
        }
        
        try:
            print(f"📤 Posting to m/{submolt}: {content[:50]}...")
            resp = self.session.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("⏳ Rate Limit Hit! Cooling down...")
            else:
                print(f"❌ Post failed: {e}")
            return None

    def reply_to_post(self, content, parent_id, submolt="general"):
        """
        Reply to a specific post.
        """
        # Self-Sanitize Outgoing
        content = ContentSanitizer.sanitise(content)
        
        url = f"{self.BASE_URL}/posts"
        payload = {
            "content": content,
            "parent_id": parent_id,
            "submolt": submolt
        }
        
        try:
            print(f"📤 Replying to {parent_id}: {content[:50]}...")
            resp = self.session.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("⏳ Rate Limit Hit! Cooling down...")
            else:
                print(f"❌ Reply failed: {e}")
            return None

    def get_notifications(self):
        """Check for mentions or replies."""
        url = f"{self.BASE_URL}/notifications"
        try:
            resp = self.session.get(url)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return []
