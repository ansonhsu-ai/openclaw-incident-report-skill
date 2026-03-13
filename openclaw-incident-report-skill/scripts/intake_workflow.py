#!/usr/bin/env python3
"""
Orchestrates the Strict mode intake workflow:
1. Receives raw incident path.
2. Runs the local sanitization logic.
3. Runs the review script.
4. If clean, echoes success, meaning the LLM may now ingest the output file.
"""

import sys
import subprocess
import argparse
import os

def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"ERROR: File {filepath} does not exist.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Strict Mode Incident Intake Workflow")
    parser.add_argument("--input", "-i", required=True, help="Raw incident text file")
    parser.add_argument("--output", "-o", required=True, help="Sanitized output text file")
    args = parser.parse_args()

    check_file_exists(args.input)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sanitize_script = os.path.join(script_dir, "sanitize.py")
    review_script = os.path.join(script_dir, "review_sanitized.py")
    
    print("--- 1. Running Strict Sanitization ---")
    ret_san = subprocess.run([sys.executable, sanitize_script, "-i", args.input, "-o", args.output])
    if ret_san.returncode != 0:
        print("ERROR: Sanitization failed.")
        sys.exit(1)
        
    print("\n--- 2. Running Post-Sanitization Review ---")
    ret_rew = subprocess.run([sys.executable, review_script, "-i", args.output])
    if ret_rew.returncode != 0:
        print("ERROR: Safety review failed. Unredacted sensitive information was detected!")
        sys.exit(1)
        
    print("\n--- Strict Intake Complete ---")
    print(f"SUCCESS: The file '{args.output}' is cleanly sanitized and ready for LLM ingestion.")

if __name__ == "__main__":
    main()
