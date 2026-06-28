---
name: agent-skills-github-sync
description: "Use when synchronizing Hermes Agent local skills with a remote GitHub repository. Guides the backup, management, and deployment of agent skills."
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [skills, github, backup, deploy, hermes-agent]
    related_skills: [github-repo-management, hermes-agent]
---

# Agent Skills GitHub Synchronization

## Overview
This skill outlines the process for exporting local Hermes Agent skills, structuring them for repository storage, and pushing/pulling them to/from a GitHub repository. It acts as a guide for keeping skills synchronized between Tonthong (and other AI agents) and a central GitHub repository.

## When to Use
- When you want to back up your current local skills (`~/.hermes/skills/`) to GitHub.
- When you need to sync skills from GitHub back into a new or existing Hermes environment.
- When sharing customized skills with other agents.

## Directory Mapping
- **Local Source:** `~/.hermes/skills/`
- **Repo Destination:** `skills/` within your cloned repository (e.g., `ai-skills/skills/`).

## Synchronization Process

### 1. Exporting Local Skills to Repo
To update your repository with local skills:
```bash
# Define paths
REPO_DIR="$HOME/ai-skills"
LOCAL_SKILLS_DIR="$HOME/.hermes/skills"

# Copy new and modified skills (excluding dotfiles/caches)
rsync -av --exclude '.*' "$LOCAL_SKILLS_DIR/" "$REPO_DIR/skills/"

# Verify status in git
cd "$REPO_DIR"
git status
```

### 2. Pushing Changes to GitHub
```bash
git add skills/
git commit -m "sync: updated agent skills $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
git push origin main
```

### 3. Deploying/Importing Skills from Repo
To apply skills from GitHub back into the local environment:
```bash
# Pull latest from Git
cd "$REPO_DIR"
git pull origin main

# Sync to local skills dir
rsync -av --exclude '.*' "$REPO_DIR/skills/" "$LOCAL_SKILLS_DIR/"

# Note: Active sessions cache skills; start a new session or restart the agent service if needed
```

## Common Pitfalls
1. **Syncing caches or private configs:** Always exclude dotfiles/lockfiles (like `.usage.json`, `.curator_state`, `.bundled_manifest`, and lockfiles) during sync.
2. **Commit conflicts:** Always pull before pushing when working across multiple environments.
3. **Session Cache:** Changing local files directly requires starting a new session or running `hermes status` / reloading to update active memory in some setups.
4. **Git Author Identity Errors:** In a clean or containerized VPS environment, git commits may fail with "Author identity unknown". Always ensure `git config user.name` and `git config user.email` are configured (locally or globally) before attempting to commit.
5. **README.md must be included in every sync:** The file `/home/thaieasyvps/.hermes/skills/README.md` is the TOC for `github.com/SatangTheValue/ai-skills`. Always `git add skills/ README.md` — not just `skills/` — so the index stays current after skill additions.

## Verification Checklist
- [ ] No dotfiles (e.g., `.usage.json`) copied to repository `skills/` folder
- [ ] Git commit message specifies the timestamp of synchronization
- [ ] `git push` command finishes successfully with exit code 0
