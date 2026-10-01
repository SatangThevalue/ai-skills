#!/usr/bin/env python3
"""Scanner for identifying credentials, tokens, and passwords in skill repositories."""

import argparse
import os
import re
import sys

PATTERNS = [
    (r"[0-9]{9,11}:[A-Za-z0-9_-]{35}", "Telegram Bot Token"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI / LLM API Key"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    (r"EAAG[a-zA-Z0-9]+", "Facebook Graph API Token"),
    (r"(?:password|secret|key)\s*[:=]\s*['\"][A-Za-z0-9@#$%^&*_+=-]{8,}['\"]", "Hardcoded Secret/Password"),
]

EXCLUDE_PATTERNS = [
    "your_",
    "your-",
    "<",
    ">",
    "xxx",
    "placeholder",
    "example",
    "dummy",
    "...",
    "***",
    "test",
    "secret_key",
    "mysecret",
    "here",
    "key_here",
    "not-needed",
]


def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return findings

    for line_num, line in enumerate(lines, start=1):
        for rgx, label in PATTERNS:
            matches = re.findall(rgx, line, re.IGNORECASE)
            for m in matches:
                m_str = str(m)
                if any(ex in m_str.lower() for ex in EXCLUDE_PATTERNS):
                    continue
                findings.append((line_num, label, m_str))
    return findings


def main():
    parser = argparse.ArgumentParser(description="Scan skill files for exposed secrets")
    parser.add_argument("--path", required=True, help="Directory to scan")
    args = parser.parse_args()

    target_dir = os.path.abspath(os.path.expanduser(args.path))
    if not os.path.exists(target_dir):
        print(f"Error: Path {target_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Scanning {target_dir} for exposed secrets...")
    total_leaks = 0

    for root, dirs, files in os.walk(target_dir):
        if any(skip in root for skip in [".git", ".curator_backups", "__pycache__"]):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            findings = scan_file(file_path)
            if findings:
                total_leaks += len(findings)
                rel_path = os.path.relpath(file_path, target_dir)
                print(f"\n[ALERT] {rel_path}:")
                for line_num, label, match in findings:
                    masked = match[:4] + "..." + match[-4:] if len(match) > 10 else "***"
                    print(f"  Line {line_num} [{label}]: {masked}")

    if total_leaks == 0:
        print("\n[+] SUCCESS: No exposed credentials found.")
        sys.exit(0)
    else:
        print(f"\n[-] WARNING: Found {total_leaks} potential leak(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
