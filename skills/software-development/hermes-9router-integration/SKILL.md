---
name: hermes-9router-integration
description: "Deploy 9Router and integrate it with Hermes Agent profiles."
version: 0.1.0
metadata:
  hermes:
    tags: [9Router, LLM, Proxy, Multi-Profile, Docker, Tailscale]
---

# Hermes 9Router Integration

This skill deploys 9Router via Docker and integrates it with Hermes Agent profiles. It covers handling API key requirements, configuring separate API keys per profile for tracking, and ensuring correct endpoint URL formatting for remote access via Tailscale. It does NOT cover configuring upstream providers within 9Router itself.

## When to Use
- When deploying 9Router alongside Hermes Agent.
- When configuring Hermes to use 9Router as its LLM provider.
- When you need separate API keys for different Hermes profiles to track usage individually.
- When troubleshooting `401 API key required for remote API access` errors from 9Router.

## Prerequisites
- Docker and Docker Compose installed.
- Tailscale IP known (if accessing remotely).
- Infisical Vault configured for secret management (CRITICAL RULE: update both Vault and Hermes config).

## Quick Reference
- **9Router Port**: `20128`
- **Dashboard URL**: `http://<IP>:20128/dashboard`
- **API URL**: `http://<IP>:20128/v1`
- **Default Password**: `123456`

## Procedure

### 1. Deploy 9Router via Docker
Invoke through the `terminal` tool:
Create `docker-compose.yml` for 9Router by reproducing the provided template:
`skill_manage(action='write_file', name='hermes-9router-integration', file_path='templates/docker-compose.yml')`
*(See `templates/docker-compose.yml` for a clean, comment-safe deployment config).*
Do NOT use inline comments next to environment variables in your own YAML, as they break Docker's `.env` parsing.

Run it: `docker compose up -d`

### 2. Configure 9Router Settings via SQLite (Optional/Troubleshooting)
If the dashboard is inaccessible or you need to force settings, invoke through `terminal`:
```bash
docker exec satang-9router apk add sqlite -q
docker exec satang-9router sqlite3 /app/data/db/data.sqlite "UPDATE settings SET data = json_set(data, '$.requireApiKey', false) WHERE id = 1;"
```

### 3. Integrate with Hermes Profile
Ensure you use the FULL API key generated from the 9Router dashboard. The SQLite database truncates the display of the key (e.g., `sk-8a2...158a`), but the actual key is the full string.
For a specific profile (e.g., `crassula`):
1. `terminal` -> `hermes --profile crassula config set providers.9router.url "http://100.115.66.121:20128/v1"`
2. `terminal` -> `hermes --profile crassula config set providers.9router.api_key "<FULL_API_KEY>"`
3. `terminal` -> `hermes --profile crassula config set default_provider "9router"`
4. `terminal` -> `hermes --profile crassula config set default_model "<MODEL_NAME>"`

### 4. Restart Hermes Gateway
You MUST restart the Hermes Gateway for the profile changes to take effect. If you are the agent, instruct the user to run this outside the agent session:
`hermes gateway restart`

## Pitfalls
- **API Key Required for Remote Access**: Even if `Require API key` is disabled in the 9Router dashboard, 9Router HARD-CODES a requirement for an API key if the request comes from a remote IP (like a Tailscale IP). You MUST configure an API key in Hermes.
- **Port Binding Warning**: Changing `100.115.66.121:20128:20128` to `20128:20128` to allow all IPs triggers the dashboard's "remote access" password enforcement. The `INITIAL_PASSWORD` environment variable must be set in `docker-compose.yml`, or you will be locked out of the dashboard.
- **Provider Quota/Rate Limits**: If 9Router returns a `503 Service Unavailable` with `429 Resource Exhausted` from the upstream provider, the quota is empty. The agent must switch to a fallback model/provider (e.g. `cli-proxy-api`) immediately via chat command `/model <fallback>` or `hermes config set`.
- **API Key Configuration Error**: When configuring the 9Router API key for a profile, ensure you use `api_key: <key>` and NOT `api_key_env_var: <key>` if providing the raw key string. `api_key_env_var` expects an environment variable *name*. If you put the key directly in `api_key_env_var`, the agent throws `unknown config keys ignored: api_key_env_var` and fails to authenticate because it has no actual key.
- **Truncated API Keys in DB**: If you query the `apiKeys` table in 9Router's SQLite DB, the `key` column displays a truncated version (e.g., `sk-8a2...158a`). Do NOT use this truncated string in Hermes config. You must use the FULL key provided by the 9Router dashboard.
- **Docker Compose Environment Variables**: Do not put comments on the same line as environment variables in `docker-compose.yml` (e.g., `- REQUIRE_API_KEY=*** # comment`). Docker will include the comment in the variable value, causing failures.
- **INITIAL_PASSWORD Issues**: Sometimes setting `INITIAL_PASSWORD` via environment variables fails. If you cannot log in, remove the variable, recreate the container, and use the default password (`123456`) to log in and change it via the dashboard.

## Verification
Test the 9Router chat completions endpoint directly:
```bash
curl -s http://100.115.66.121:20128/v1/chat/completions \
  -H "Authorization: Bearer *** \
  -H "Content-Type: application/json" \
  -d '{"model":"ag/gemini-3.1-pro-low","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```