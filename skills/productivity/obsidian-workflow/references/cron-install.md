# One-line example to install cron entry (user-level) to run git_push_cron.sh every 15 minutes
# Run from the vault directory
CRON_CMD="$HOME/Documents/Obsidian Vault/scripts/git_push_cron.sh"
(crontab -l 2>/dev/null | grep -v -F "$CRON_CMD" || true) | { cat; echo "*/15 * * * * $CRON_CMD >/dev/null 2>&1"; } | crontab -
