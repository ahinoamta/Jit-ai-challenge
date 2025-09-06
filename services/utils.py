import re

def sanitize_input(text):
    # Remove dangerous shell characters
    return re.sub(r'[;&|`$<>]', '', text)

def is_prompt_injection(text):
    # Simple check for prompt injection patterns
    return any(trigger in text.lower() for trigger in ["ignore previous", "disregard above", "as an ai", "you are now"])
