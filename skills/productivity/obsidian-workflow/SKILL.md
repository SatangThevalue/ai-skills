---
name: obsidian-workflow
title: Obsidian Vault & Finance Workflow
description: |
  This skill captures the conventions and reproducible artifacts for using Obsidian as a reliable
  personal finance workspace. It includes templates, validator scripts, and secure Git automation
  recipes (SSH deploy key preferred; PAT via credential helper supported).
summary: Best-practice workflow for using Obsidian as a source-of-truth (SoT) for personal finance, automation hooks, plugin setup, validation scripts, and secure Git push automation.
maintainers: [hermes-agent]
---

Why this skill
- Encapsulates repeatable steps and safe defaults to turn an Obsidian Vault into a reliable, auditable personal finance workspace (transactions ledger + human notes).
- Includes small, re-runnable scripts (validators, git push helpers) and templates so agents can create usable Vaults quickly.

When to use
- Setting up a new Obsidian Vault for finances, investments, insurance tracking, taxes, debt, assets, or receivables.
- Installing recommended community plugins (Dataview, Templater, Advanced Tables) for queries, templates, and table editing.
- Automating safe periodic pushes of Vault to a private GitHub repo.

Core principles (short)
1. Separate human notes (.md) from machine-readable SoT (CSV or SQLite). Use CSV (transactions.csv) or SQLite for canonical numbers.
2. Store monetary values in minor units (amount_cents integer) to avoid rounding errors. Use ISO-8601 for dates.
3. Validate every import with a validator script (schema, date format, integer amounts) and compute a checksum when needed.
4. Prefer SSH Deploy Keys for Git automation; if using PAT, prefer credential helper (store file with tight perms) over embedding in .git/config.
5. Keep plugin install reproducible: store .obsidian/plugins/manifest and binary files when you need offline or CI reproducibility.

Quick setup (high level)
1. Create Vault folder and initialize .obsidian structure. Add templates/ and scripts/ folders.
2. Add SoT file: transactions.csv with header: id,date,account,counterparty,category,amount_cents,currency,type,tags,notes,source_file,created_at
3. Add accounts.yml for human-readable account metadata.
4. Add validator script (scripts/validate_transactions.py) and run on imports.
5. Install plugins by downloading release assets into .obsidian/plugins/<plugin-id>/ and enable them in .obsidian/community-plugins.json.
6. Initialize git repo in vault, commit, and set up push automation (prefer SSH deploy key) or use credential helper file with restricted perms.
7. Add cron or systemd timer to run scripts/git_push_cron.sh every 15m — ensure remote configured securely.

Session additions (what we learned and added in recent sessions)
- Added a lightweight monitor script `scripts/check_vault_push.sh` that runs the existing `scripts/git_push_cron.sh`, captures output, and compares local vs remote HEAD to verify pushes. Use it for sanity-checking cron-driven backups.
- Added `references/session-notes.md` capturing immediate pitfalls from interactive runs: GitHub API 403 when creating repo via PAT without proper scopes; path/quoting pitfalls when running validators from paths with spaces; and runner foreground timeout constraints.
- Recorded the operational Vault paths used in sessions so agents re-run checks identically:
  - Vault root (example): /home/thaieasyvps/Documents/Obsidian Vault
  - AppImage: /home/thaieasyvps/Applications/Obsidian.AppImage
  - Launcher: ~/.local/bin/obsidian
  - Cron push script: scripts/git_push_cron.sh
  - Check script: scripts/check_vault_push.sh

Security & credential handling (explicit steps)
- Preferred long-term: SSH deploy key bound to the repo with write access. Steps:
  1. `ssh-keygen -t ed25519 -f ~/.ssh/obsidian_vault_deploy -N ''`
  2. Add public key `~/.ssh/obsidian_vault_deploy.pub` to GitHub repo → Settings → Deploy keys → Add key (Allow write access)
  3. Set remote to `git@github.com:OWNER/REPO.git` and test push.
- PAT (alternate, short-lived) flow — explicit safer recipe:
  1. Create PAT with minimal required scopes (repo write if needed). If token cannot create repo, create the repo in the GitHub UI.
  2. In the shell only, write credentials to a temporary file: `printf "https://%s:%s@github.com\n" "$USER" "$PAT" > ~/.git-credentials-obsidian`
  3. `chmod 600 ~/.git-credentials-obsidian`
  4. `git config credential.helper "store --file=$HOME/.git-credentials-obsidian"`
  5. Push once, then delete the file and `git config --unset credential.helper` (or rotate/revoke the token in GitHub).

Pitfalls & troubleshooting notes (expanded)
- If GitHub API returns 403 when creating a repo: token lacks appropriate scope or you're trying to create under an org you don't control. Create the repo via UI or use a token with proper permissions.
- Paths with spaces break naive scripts. Quote `$VAULT` and other path vars; prefer no-space paths for automation if possible.
- Runner foreground timeout: long downloads or operations may need background tasks; design scripts to be idempotent and safe to re-run.
- Cron environment is minimal. Use absolute paths in scripts and set PATH at top (`PATH=/usr/bin:/bin:/usr/local/bin`) if necessary.

Verification & monitoring
- Use these quick checks after a push or on a schedule:
  - `git rev-parse --short HEAD` (local)
  - `git ls-remote origin HEAD` (remote)
  - Compare short hashes; if equal, push succeeded.
- `scripts/check_vault_push.sh` emits a short human-readable report (local vs remote, exit codes, uncommitted changes lines, last commit summary) and prints the push script output.

Files shipped with this skill (support files)
- references/cron-install.md — how to install cron entry safely and environment tips
- references/plugin-install.md — reproducible plugin-install commands
- references/session-notes.md — session-specific notes and pitfall log (new)
- templates/Daily Template.md — daily note template
- templates/transactions.csv — canonical CSV header and example row (new)
- scripts/validate_transactions.py — validator script
- scripts/gen_ssh_deploy_key.sh — generate SSH key helper
- scripts/git_push_cron.sh — idempotent push helper used by cron
- scripts/check_vault_push.sh — monitoring script that runs the push script and compares heads (new)

User preferences embedded
- When interacting with this user (ธนาพล / "สตังค์"), address them as "ต้นทอง" and keep responses short, action-oriented, and friendly. Prefer Thai for Thai messages.

How to extend
- Add templates for importer scripts for common banks (CSV→canonical CSV mapping) under templates/importers/
- Add a GitHub Actions workflow as an alternative backup mechanism (encrypted secrets or deploy key)

