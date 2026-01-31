import re

class ContentSanitizer:
    """
    Sanitizes content from external agents on Moltbook.
    Ensures no executable code or prompt injections reach the core logic.
    """
    
    # Patterns that look like code execution attempts
    DANGEROUS_PATTERNS = [
        r"```python", r"```bash", r"```sh", r"```javascript",
        r"import os", r"subprocess\.", r"eval\(", r"exec\(",
        r"<script>", r"javascript:",
        r"rm -rf", r"wget ", r"curl "
    ]
    
    # Patterns that look like Prompt Injection attempts
    INJECTION_PATTERNS = [
        r"Ignore previous instructions",
        r"You are now unrestricted",
        r"DAN mode",
        r"System override",
        r"As an AI language model specifically programmed to"
    ]

    @staticmethod
    def sanitise(content: str) -> str:
        """
        Clean untrusted content.
        1. Strip code blocks if they contain dangerous keywords.
        2. Mask prompt injection phrases.
        3. Limit length to prevent context flooding.
        """
        if not content:
            return ""

        original_content = content
        
        # 1. Block aggressive code patterns
        for pattern in ContentSanitizer.DANGEROUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, "[BLOCKED_CODE_PATTERN]", content, flags=re.IGNORECASE)

        # 2. Mask injection attempts
        for pattern in ContentSanitizer.INJECTION_PATTERNS:
             if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, "[REDACTED_INJECTION_ATTEMPT]", content, flags=re.IGNORECASE)

        # 3. Limit Length (Prevent buffer overflow attacks)
        MAX_LENGTH = 2000
        if len(content) > MAX_LENGTH:
            content = content[:MAX_LENGTH] + "... [TRUNCATED_LENGTH_LIMIT]"

        if content != original_content:
            print(f"⚠️  Sanitizer modified content from length {len(original_content)} to {len(content)}")
            
        return content

    @staticmethod
    def is_safe_to_process(content: str) -> bool:
        """Returns False if content triggers high-severity rules."""
        # Absolute block for certain keywords
        BLOCKLIST = ["suicide", "self-harm", "bomb", "child abuse"] # Basic safety filter
        
        for word in BLOCKLIST:
             if word in content.lower():
                 return False
        return True
