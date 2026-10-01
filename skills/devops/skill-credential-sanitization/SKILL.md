---
name: skill-credential-sanitization
description: Sanitize credentials and secrets in skill repositories.
version: 0.1.0
metadata:
  hermes:
    tags: [Security, Sanitization, Git, Skills]
---

# Skill Credential Sanitization

Audits skill files and associated Git repositories for hardcoded credentials, bot tokens, and passwords, replacing them with dynamic environment lookups or safe placeholders. It does not handle key rotation on third-party provider dashboards. Relies on Python standard library and Git.

## When to Use
- "ตรวจหารหัสผ่านในไฟล์สกิล" / "ลบโทเค็นออกจาก repo"
- Credentials or tokens were accidentally written into `SKILL.md` or scripts.
- Pre-push security sweep before syncing `~/.hermes/skills/` to remote repositories.
- Cleaning up exposed Telegram bot tokens, database passwords, or API secrets.

## Prerequisites
- Git repository clone with write permissions (e.g. `~/ai-skills`).
- Local skills directory located at `~/.hermes/skills/`.
- Python 3 with standard library.

## How to Run
Execute the scanning script `scripts/scan_secrets.py` through the `terminal` tool. Replace leaked values using `patch` or Python standard file operations, then commit and push.

## Quick Reference
```bash
python3 ~/.hermes/skills/devops/skill-credential-sanitization/scripts/scan_secrets.py --path ~/.hermes/skills
python3 ~/.hermes/skills/devops/skill-credential-sanitization/scripts/scan_secrets.py --path ~/ai-skills/skills
git diff --cached | grep -iE "(token|password|secret|key)\s*="
git commit -m "fix(security): sanitize hardcoded credentials"
git push origin main
```

## Procedure

1. **Scan for Hardcoded Credentials**
   Run the scanner across local and repository skill trees using the `terminal` tool:
   ```bash
   python3 ~/.hermes/skills/devops/skill-credential-sanitization/scripts/scan_secrets.py --path /home/thaieasyvps/ai-skills/skills
   python3 ~/.hermes/skills/devops/skill-credential-sanitization/scripts/scan_secrets.py --path /home/thaieasyvps/.hermes/skills
   ```

2. **Replace Hardcoded Secrets with Dynamic Lookups**
   In Python files, replace static tokens with `os.getenv()` calls:
   ```python
   # Replace: bot_token = "123456789:ABC..."
   # With:
   import os
   bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
   ```
   In Markdown documentation (`SKILL.md`), replace raw credentials with uppercase generic placeholders like `<TELEGRAM_BOT_TOKEN>` or `<API_KEY>`.

3. **Verify Staged Changes**
   Stage modifications in the Git repository and inspect the staged diff to ensure no new secrets are introduced:
   ```bash
   cd ~/ai-skills
   git add -A
   git diff --cached | grep -iE "(password|token|secret|key)\s*=\s*['\"][^'\"]{6,}['\"]" || echo "CLEAN"
   ```

4. **Synchronize Catalog and Push**
   Run the TOC indexer, rsync the changes to maintain library consistency, commit, and push:
   ```bash
   python3 ~/.hermes/skills/hermes-agent/multi-profile-skills-sync/scripts/sync_skills_index.py
   rsync -av --delete --exclude='.git' /home/thaieasyvps/.hermes/skills/ /home/thaieasyvps/ai-skills/skills/
   cd ~/ai-skills
   git add .
   git commit -m "fix(security): sanitize hardcoded credentials across skills"
   git push origin main
   ```

## Pitfalls
- **Accidental Re-introduction via rsync:** If credentials are removed from `~/ai-skills` but remain in `~/.hermes/skills`, a subsequent rsync will copy the leaked secrets back. Always sanitize `~/.hermes/skills` first.
- **Git Commit Amending on Pushed Commits:** Amending a commit already pushed to a protected remote branch requires `--force-with-lease`, which may trigger security blocks. Preferred approach is committing a clean forward fix on top of the HEAD.
- **False Negatives on Non-Standard Secrets:** Standard regexes catch common formats (Telegram tokens, OpenAI keys), but unique passwords require targeted substring scanning.

## Verification
Confirm that zero high-entropy secrets or bot tokens exist in the repository:
```bash
cd ~/ai-skills && git grep -E "[0-9]{9,11}:[A-Za-z0-9_-]{35}" && echo "LEAK DETECTED" || echo "SUCCESS: No tokens found"
```
