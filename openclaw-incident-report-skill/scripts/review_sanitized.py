#!/usr/bin/env python3
"""
Reviews sanitized text to detect potential leftover sensitive information
before it reaches an LLM.

This acts as a second-pass safety check.
"""
import re
import argparse
import sys

import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# We reuse the same core patterns but perhaps we look for generic hints.
# Since sanitize.py replaces them with [REDACTED_XXX], we can check if any *unredacted*
# patterns are still present.
from sanitize import PATTERNS

def review_text(text: str) -> list:
    """Check text for unredacted sensitive patterns and return warnings."""
    warnings = []
    
    # Check for known patterns that should have been redacted
    for key, (pattern, _) in PATTERNS.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            matched_str = str(match.group(0))
            if "[REDACTED" not in matched_str:
                warnings.append(f"Found potential unredacted {key}: {matched_str[:4]}... (truncated)")

    # Additional heuristics: Look for the word "secret", "password", "token" near non-redacted blocks
    # just as a general warning.
    heuristic_pattern = r"(?i)\b(password|secret|token|api_key|credential)\b.{0,20}?([^\[\]\s]{5,})"
    for match in re.finditer(heuristic_pattern, text):
        val = str(match.group(2))
        if "REDACTED_" not in val and len(val) > 8:
            warnings.append(f"Heuristic warning: Found word '{str(match.group(1))}' near potential secret: '{val[:4]}...'")

    return warnings

def main():
    parser = argparse.ArgumentParser(description="Review sanitized text for leftovers.")
    parser.add_argument("--input", "-i", required=True, help="Input sanitized file to review")
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()
        
    warnings = review_text(content)
    
    if warnings:
        print("WARNING: The sanitized file may still contain sensitive data. Review manually!")
        for w in warnings:
            print(f" - {w}")
        sys.exit(1)
    else:
        print("Review passed: No obvious unredacted sensitive patterns detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
