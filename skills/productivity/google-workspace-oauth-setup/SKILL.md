---
name: google-workspace-oauth-setup
description: "Process for enabling Hermes access to personal Google accounts."
version: 0.1.0
metadata:
  hermes:
    tags: [Google, OAuth, Workspace, Authentication, Setup]
---

# Google Workspace OAuth Setup

This skill captures the end-to-end workflow for authenticating Hermes Agent with a personal Google account via an external Desktop OAuth client. It covers receiving the `client_secret.json` from the user, generating the authorization URL, and completing the OAuth handshake to generate the `google_token.json` credential file. It does NOT cover using the APIs post-setup.

## When to Use
- When the user provides a `client_secret_*.json` file from Google Cloud Console.
- When the `google-workspace` skill reports missing credentials or `NOT_AUTHENTICATED`.
- When connecting Hermes to a personal `@gmail.com` account for Calendar, Docs, or Gmail access.

## Prerequisites
- The user must create an OAuth 2.0 "Desktop app" client in Google Cloud Console.
- The user must add their email to the "Test users" list under OAuth consent screen (if the app is in Testing mode).
- The `google-workspace` skill must be installed.

## Quick Reference
- **Client Secret Setup**: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --client-secret <PATH>`
- **Generate Auth URL**: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-url`
- **Exchange Code**: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-code "<URL_OR_CODE>"`
- **Check Status**: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check`

## Procedure

### 1. Save the Client Secret
When the user uploads or pastes the content of their `client_secret.json` file, save it to a secure location (e.g., inside the workspace). Then invoke through the `terminal` tool:
```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --client-secret /path/to/the/client_secret.json
```
The script will copy and format this into `~/.hermes/google_client_secret.json`.

### 2. Generate the Authorization URL
Invoke through the `terminal` tool to generate the link the user needs to click:
```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-url
```
Extract the URL from the output and provide it directly to the user. Inform the user:
> 1. Open this link in your browser and log in.
> 2. If warned "App isn't verified", click "Advanced" -> "Go to... (unsafe)".
> 3. After granting permission, the page will fail to load (`localhost refused to connect`). This is expected.
> 4. Copy the ENTIRE URL from your address bar and paste it back to me.

### 3. Complete the OAuth Handshake
Once the user provides the redirected `http://localhost:1/?state=...` URL, invoke through the `terminal` tool:
```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-code "<THE_URL_PROVIDED_BY_USER>"
```
This will exchange the code for a refresh token and save it to `~/.hermes/google_token.json`.

## Pitfalls
- **Test Users Limit**: For personal Google accounts, the OAuth app is usually in "Testing" mode. If the user's email is not explicitly added to the "Test users" list in Google Cloud Console, they will hit an `Error 403: access_denied` when clicking the auth URL.
- **7-Day Token Expiration in Testing Mode**: When the GCP project publishing status is "Testing", refresh tokens expire after exactly 7 days, resulting in `TOKEN_REVOKED: invalid_grant: Token has been expired or revoked`. To prevent weekly re-authentication, publish the app to "In production" in Google Cloud Console.
- **Service API Enablement Required**: Granting OAuth scope consent does NOT automatically enable the underlying service in Google Cloud Console. If calling an API (e.g., Tasks, People, Sheets) fails with `HttpError 403: ... API has not been used in project ... before or it is disabled`, navigate to `https://console.developers.google.com/apis/api/<service>.googleapis.com/overview?project=<project_id>` and click **Enable**.
- **Google Tasks Scope in setup.py**: The default `SCOPES` list in `setup.py` must include `https://www.googleapis.com/auth/tasks` if task synchronization or management is required.
- **Combined Arguments**: The `setup.py` script enforces separate invocations. Do NOT pass `--client-secret` and `--auth-url` in the same terminal command.
- **Localhost Refusal**: The user will see `ERR_CONNECTION_REFUSED` or `This site can't be reached` on `localhost:1` after approving access. This is completely normal for Desktop OAuth flows; the vital information is the `code=` parameter embedded in that URL.

## Verification
Invoke through the `terminal` tool to ensure the token is active:
```bash
python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
```
It should return `AUTHENTICATED: Token valid`.