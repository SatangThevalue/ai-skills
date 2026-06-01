# Session Notes — Vault setup highlights

Date: 2026-06-01

Summary of actions taken in-session:
- Created Obsidian AppImage and launcher for local use.
- Created Vault at: /home/thaieasyvps/Documents/Obsidian Vault and initialized git repo.
- Added templates and validator script; created transactions.csv in vault root as canonical ledger.
- Installed cron job to run scripts/git_push_cron.sh every 15 minutes.
- Implemented check_vault_push.sh monitor and README, added initial README.md and pushed to GitHub repo SatangThevalue/my-vault-repo.

Pitfalls observed and remedies:
- GitHub API 403 on repo creation: token lacked scope — remedy: create repo via UI or use token with repo scope.
- Paths with spaces can break scripts; always quote variables and prefer no-space folder names for automation.
- Do not persist PATs in repo. If used to bootstrap, store in temporary file with `chmod 600` and delete after use.
- Runner foreground timeout: long downloads must be run in background or split into smaller steps.

Short checklist for next runs:
- Verify cron entries and ensure scripts use absolute paths.
- Offer SSH deploy key flow as default for long-term automation.
