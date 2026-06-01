# Quick setup notes — observed behavior and recommended commands

This short reference captures the exact sequence and command-line behavior observed during a 2026-06-01 session where an OAuth client_secret JSON was installed and an auth URL generated.

Principles
- The included `setup.py` runs a small CLI with separate steps: (1) register client secret path, (2) request an auth URL, (3) exchange auth code. Do these as separate invocations.
- Do NOT pass `--auth-url` on the same invocation as `--client-secret` — the script's argparse rejects that combination.
- The script does not accept `--services` or `--format` flags in the current implementation; `--auth-url` will request the default scope set encoded in the script.

Typical commands (run from any shell):

1. Save the client secret JSON to the hermes-managed location (script does this for you):

python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py --client-secret /path/to/client_secret.json

Expected output:
OK: Client secret saved to ~/.hermes/google_client_secret.json

2. Request the authorization URL (returns a single URL on stdout):

python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py --auth-url

- Open the returned URL in the browser (use the Google account you want to grant access).
- Approve consent (the redirect will attempt to hit http://localhost:1 and usually fail; this is expected).
- Copy the entire redirect URL from the browser address bar (it contains the `code=` parameter), or copy only the code value.

3. Exchange the code for tokens:

python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py --auth-code "PASTED_URL_OR_CODE"

Expected token location (after success):
- ~/.hermes/google_token.json  (access + refresh tokens)

Scopes observed in the session (the script's default):
- https://www.googleapis.com/auth/gmail.readonly
- https://www.googleapis.com/auth/gmail.send
- https://www.googleapis.com/auth/gmail.modify
- https://www.googleapis.com/auth/calendar
- https://www.googleapis.com/auth/drive
- https://www.googleapis.com/auth/contacts.readonly
- https://www.googleapis.com/auth/spreadsheets
- https://www.googleapis.com/auth/documents

Security notes
- Never paste client_secret.json contents into chat. Pass the file path or upload the file through a secure channel. The script saves a hermes-managed copy in ~/.hermes/google_client_secret.json.
- Token file (~/.hermes/google_token.json) contains refresh tokens — treat as sensitive.
- If you need to revoke, use the script's `--revoke` action.

Troubleshooting
- Error: `argument --auth-url: not allowed with argument --client-secret` → run `--client-secret` first, then run `--auth-url` in a separate command.
- Error: `unrecognized arguments: --services all --format json` → current setup.py does not accept those flags; call `--auth-url` and allow the default scope set or modify setup.py to accept service flags.
