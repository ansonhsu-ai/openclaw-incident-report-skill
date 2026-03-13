#!/usr/bin/env python3
"""
Locally sanitizes and de-identifies incident report notes or data BEFORE
it is sent to the LLM. This ensures sensitive PII, credentials, or 
internal tokens are scrubbed locally.
"""
import re
import argparse

PATTERNS = {
    # Match standard email addresses
    "email": (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]"),
    
    # Match various forms of phone numbers (Taiwan formats: 09xx-xxxxxx, (02)xxxx-xxxx, etc.)
    "phone": (r"(?<!\d)(09\d{2}-?\d{6}|\(0\d\)\d{4}-?\d{4}|0\d-\d{4}-?\d{4})(?!\d)", "[REDACTED_PHONE]"),
    
    # Match IPv4 addresses
    "ipv4": (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED_IP]"),
    
    # Match MAC addresses
    "mac": (r"\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b", "[REDACTED_MAC]"),
    
    # Match UUIDs typically used as identifiers or secrets
    "uuid": (r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b", "[REDACTED_UUID]"),
    
    # Match generic standalone bearer tokens
    "bearer_token": (r"(?i)(Bearer\s+)[A-Za-z0-9\-\._~\+\/]{20,}={0,2}", r"\1[REDACTED_TOKEN]"),
    
    # General assignment or key-value style secrets (e.g. api_token=..., apiKey: ..., credentials=)
    "kv_secrets": (r"(?i)((?:api[_-]?token|api[_-]?key|bearer(?:[_-]?token)?|secret|password|credentials?|token)[\"'\s]*[:=][\s\"']*)([^\"'\s\\]+)", r"\1[REDACTED_SECRET_VALUE]"),
    
    # Identity card number (Taiwan: A123456789)
    "id_card": (r"\b[A-Z][12]\d{8}\b", "[REDACTED_ID_CARD]"),
}

def sanitize_text(text: str) -> str:
    """Apply all regex patterns to replace sensitive data in text."""
    for key, (pattern, replacement) in PATTERNS.items():
        text = re.sub(pattern, replacement, text)
    return text

def main():
    parser = argparse.ArgumentParser(description="Sanitize text files locally before sending to LLM.")
    parser.add_argument("--input", "-i", required=True, help="Input raw text or log file containing sensitive info")
    parser.add_argument("--output", "-o", required=True, help="Output sanitized file path")
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()
        
    sanitized_content = sanitize_text(content)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(sanitized_content)

    print(f"Sanitized content successfully written to {args.output}")

if __name__ == "__main__":
    main()
