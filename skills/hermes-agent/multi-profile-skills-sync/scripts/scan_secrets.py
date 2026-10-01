#!/usr/bin/env python3
"""
Pre-commit and pre-sync secret scanner for Hermes Agent skills.
Scans skill files for bot tokens, private keys, passwords, and sensitive strings
before they are mirrored and pushed to GitHub.
"""

import os
import re
import sys

# High-confidence credential patterns
SENSITIVE_PATTERNS = [
    (r"\b[0-9]{9,11}:[A-Za-z0-9_-]{35}\b", "Telegram Bot Token"),
    (r"(?i)(?:password|passwd|initial_password)\s*[:=]\s*[\"']?([A-Za-z0-9@#%&!_]{6,})[\"']?", "Plaintext Password"),
    (r"(?i)(?:app_secret|client_secret|api_secret)\s*[:=]\s*[\"']([A-Za-z0-9+/=]{16,})[\"']", "API / Broker Secret"),
    (r"\bghp_[A-Za-z0-9]{36,}\b", "GitHub Personal Access Token"),
    (r"\bsk-[A-Za-z0-9]{20,}\b", "OpenAI / LLM API Key"),
    (r"\bAIza[0-9A-Za-z-_]{35}\b", "Google API Key"),
]

# Allowlist substrings (placeholders, dummy examples, env var templates)
ALLOWLIST = [
    "your_", "example", "placeholder", "dummy", "xxx", "token_here", "key_here",
    "password_here", "mysecret", "change_me", "${", "os.getenv", "<", ">", "..."
]

def is_allowed(val: str) -> bool:
    val_lower = val.lower()
    return any(a in val_lower for a in ALLOWLIST)

def scan_directory(base_dir: str):
    violations = []
    for root, dirs, files in os.walk(base_dir):
        if any(ignored in root for ignored in [".git", ".curator_backups", "__pycache__"]):
            continue
        for f in files:
            file_path = os.path.join(root, f)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                    for line_no, line in enumerate(fh, 1):
                        for pattern, label in SENSITIVE_PATTERNS:
                            matches = re.findall(pattern, line)
                            for match in matches:
                                text_val = match if isinstance(match, str) else match[0]
                                if not is_allowed(text_val):
                                    violations.append((file_path, line_no, label, text_val))
            except Exception as e:
                pass
    return violations

def main():
    target = os.path.expanduser("~/.hermes/skills")
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    print(f"[*] Scanning skills directory for exposed secrets: {target}...")
    violations = scan_directory(target)
    
    if violations:
        print(f"\n[!] ERROR: Found {len(violations)} sensitive credential(s) in skill files:")
        for path, line_no, label, val in violations:
            masked = val[:4] + "..." + val[-3:] if len(val) > 8 else "***"
            print(f"  - {path}:{line_no} [{label}]: {masked}")
        print("\nAction required: Replace sensitive credentials with os.getenv(...) or placeholders before syncing.")
        sys.exit(1)
    else:
        print("[+] SUCCESS: No sensitive credentials found. Skills are safe to sync and push.")
        sys.exit(0)

if __name__ == "__main__":
    main()
