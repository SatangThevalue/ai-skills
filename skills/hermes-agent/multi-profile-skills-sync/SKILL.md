---
name: multi-profile-skills-sync
description: "Sync and link agent skills across all profiles and GitHub."
version: 0.1.0
metadata.hermes.tags:
  - Hermes
  - Skills
  - MultiProfile
  - GitSync
---

# Multi-Profile Skills Synchronization and Linking

Consolidates Hermes Agent skills into organized category directories, symlinks all isolated profile skill paths to the central library for real-time sharing, and synchronizes the catalog to a Git repository. It does not alter profile-specific `.env` or configuration files.

## When to Use

- "จัดระเบียบไฟล์สกิล" / "organize skills"
- "ให้ทุกโปรไฟล์ใช้สกิลเหมือนกัน" / "share skills across profiles"
- "ซิงค์สกิลขึ้น GitHub" / "sync skills to github"
- When a profile cannot access newly installed skills from the default profile.

## Prerequisites

- Git repository cloned locally (e.g. `~/ai-skills` tracking `origin/main`).
- Git SSH/credential helper configured for non-interactive pushes.
- Python 3 with stdlib installed on the host.

## How to Run

Execute the categorization, symlinking, and git synchronization through the `terminal` tool.

## Quick Reference

- Check skills in profile: `hermes -p <profile> skills list`
- Inspect profile skills path: `ls -ld ~/.hermes/profiles/<profile>/skills`
- Run TOC generator: `python3 ~/.hermes/skills/hermes-agent/multi-profile-skills-sync/scripts/sync_skills_index.py`
- Mirror to Git workspace: `rsync -av --delete ~/.hermes/skills/ ~/ai-skills/skills/`

## Procedure

1. **Consolidate Unique Skills from Other Profiles**
   Inspect secondary profiles for unique skills before replacing folders:
   ```bash
   for p in ~/.hermes/profiles/*; do
     [ -d "$p/skills" ] && [ ! -L "$p/skills" ] && cp -rn "$p/skills/"* ~/.hermes/skills/
   done
   ```

2. **Categorize Root Skills**
   Ensure every skill folder containing `SKILL.md` is nested under a category folder (e.g., `devops`, `finance`, `software-development`):
   ```bash
   # Move orphaned root skill into target category
   mv ~/.hermes/skills/<skill-folder> ~/.hermes/skills/<category>/
   ```

3. **Symlink Profile Skills to Central Library**
   Replace secondary profile `skills/` folders with absolute symlinks pointing to `~/.hermes/skills`:
   ```bash
   for p in ton-crassula researcher reviewer writer; do
     rm -rf ~/.hermes/profiles/$p/skills
     ln -s /home/thaieasyvps/.hermes/skills ~/.hermes/profiles/$p/skills
   done
   ```

4. **Regenerate Documentation and Index**
   Invoke the index generator script through `terminal`:
   ```bash
   python3 ~/.hermes/skills/hermes-agent/multi-profile-skills-sync/scripts/sync_skills_index.py
   ```

5. **Pre-Push Secret Sanitization**
   Scan all skill directories and supporting scripts to ensure no live bot tokens, passwords, or API keys are committed:
   ```bash
   python3 ~/.hermes/skills/hermes-agent/multi-profile-skills-sync/scripts/scan_secrets.py
   ```
   Ensure any detected secrets are replaced with `os.getenv(...)` or `<PLACEHOLDER>` before staging.

6. **Sync and Push to Remote Git Repository**
   Mirror the organized skills directory to the git workspace, commit, and push:
   ```bash
   rsync -av --delete ~/.hermes/skills/ ~/ai-skills/skills/
   cd ~/ai-skills
   git add -A
   git commit -m "sync: update skills directory structure and index"
   git push origin main
   ```

## Pitfalls

- **Credential Leakage in Skill Files:** Supporting scripts (`scripts/`), references (`references/`), and templates (`templates/`) must never store raw Telegram bot tokens, broker API secrets, or passwords. Always sanitize with environment variables (`os.getenv()`) prior to syncing to GitHub.
- **Broken Relative Symlinks:** Always use absolute target paths (`/home/.../.hermes/skills`) when creating profile symlinks to avoid broken link resolutions.
- **Accidental Deletions:** Always inspect and copy unique profile-specific skills into `~/.hermes/skills/` before executing `rm -rf` on profile directories.
- **Git Hook Conflicts:** Verify TOC and README generation succeeds before pushing to prevent CI/README sync validation failures.

## Verification

Run `hermes -p <profile> skills list` to verify that secondary profiles immediately reflect the entire categorized library.
