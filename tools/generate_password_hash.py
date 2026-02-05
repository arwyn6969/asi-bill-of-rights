import hashlib
import sys

def hash_password(password: str, secret_key: str) -> str:
    """Hash a password using SHA-256 with secret key (matching backend logic)."""
    return hashlib.sha256((password + secret_key).encode()).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_password_hash.py <PASSWORD> <SECRET_KEY>")
        print("Example: python generate_password_hash.py mypassword123 supersecretkeyprod")
        sys.exit(1)
        
    pwd = sys.argv[1]
    key = sys.argv[2]
    
    print(f"Password: {pwd}")
    print(f"Secret Key: {key}")
    print(f"Hash: {hash_password(pwd, key)}")
