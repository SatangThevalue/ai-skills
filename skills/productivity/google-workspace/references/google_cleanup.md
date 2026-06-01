# Google cleanup & revoke (session-specific)

This reference documents the cleanup steps and local paths encountered while
working with Google OAuth in-session. Use it as a checklist when the user asks
to "disconnect" or "revoke" Google Workspace access.

Local files to inspect and remove (typical locations in this environment):
- ~/.hermes/google_client_secret.json  — client_secret JSON saved by setup
- ~/.hermes/google_oauth_pending.json — temporary PKCE session state
- ~/.hermes/google_token.json          — stored OAuth token (access/refresh)
- ~/.hermes/cache/documents/*client_secret*.json — uploaded client secret copies
- ~/.git-credentials-obsidian (if service used PAT for Git push related flows)
- Vault-level helper scripts: Documents/Obsidian Vault/scripts/google_sync.sh

Cron and scheduled jobs:
- Inspect crontab with `crontab -l` and remove any lines referencing google, google_sync, or google_oauth
- Check ~/.hermes/cron/ and ~/.hermes/scripts/ for scheduled helpers

Revocation steps (remote)
1. Revoke token from Google Account (if token present):
   - Visit https://myaccount.google.com/permissions
   - Find the OAuth app (Ton-tong) and click Remove Access
2. In Google Cloud Console:
   - Go to APIs & Services → Credentials
   - Delete OAuth Client ID(s) (or rotate client secret)
   - If using Service Account keys, go to IAM & Admin → Service Accounts → Keys and delete the key
3. If Domain‑wide Delegation was used, remove the client ID from Admin Console
   - Admin Console → Security → API controls → Domain wide delegation → remove client ID

Post-cleanup verification
- Ensure no `~/.hermes/google_*.json` files remain
- Run `crontab -l` to confirm no google_sync lines
- Optionally rotate GitHub PATs or remove any temporary credential files created during the session

Security notes
- Never commit client secrets or service-account keys to git.
- If a secret/key leaked during the session, rotate/revoke immediately.
