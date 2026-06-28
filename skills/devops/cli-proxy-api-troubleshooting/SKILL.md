---
name: cli-proxy-api-troubleshooting
description: "Diagnose and fix cli-proxy-api provider and auth failures."
version: 0.1.0
metadata.hermes.tags:
  - Proxy
  - Systemd
  - Troubleshooting
  - OAuth
---

# CLIProxyAPI Troubleshooting

Diagnoses and resolves issues where `cli-proxy-api` returns `unknown provider` errors or empty model lists due to corrupted authentication files. This procedure establishes a graceful systemd lifecycle to prevent future corruption and verifies end-to-end model availability.

## When to Use
- User reports `unknown provider for model` errors from a local API proxy.
- Hermes API calls to port `42869` return HTTP 502 or 404.
- `cli-proxy-api` is running but `curl http://127.0.0.1:42869/v1/models` returns `{"data":[]}`.
- Setting up or daemonizing `cli-proxy-api` on a VPS.

## Prerequisites
- `cli-proxy-api` installed (typically in `/opt/cli-proxy-api/`).
- Access to the user's home directory (configuration typically in `~/.cli-proxy-api/`).

## How to Run
Use the `terminal` tool to inspect processes, ports, and systemd status. Use the `read_file` tool to inspect configuration and log files. If Python scripting is needed to manipulate `config.yaml`, use the `execute_code` tool.

## Quick Reference
- **Check models:** `curl -sS http://127.0.0.1:42869/v1/models`
- **Test completion:** `curl -sS -X POST http://127.0.0.1:42869/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer test" -d '{"model": "gemini-3-flash", "messages": [{"role": "user", "content": "hello"}]}'`
- **Auth config path:** `~/.cli-proxy-api/*.json`
- **Error logs path:** `~/.cli-proxy-api/logs/`

## Procedure

1. **Verify the Process and Port**
   Use the `terminal` tool to ensure the proxy is running and listening:
   ```bash
   ss -ltnp | grep 42869
   ps aux | grep cli-proxy-api
   ```

2. **Inspect Proxy Logs and Model Availability**
   Use `terminal` to list models:
   ```bash
   curl -sS http://127.0.0.1:42869/v1/models
   ```
   If the `data` array is empty, the upstream providers are not configured or auth is broken. Inspect logs with `terminal`:
   ```bash
   ls -la ~/.cli-proxy-api/logs/
   tail -n 50 ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log
   ```

3. **Check for Auth File Corruption**
   Use `terminal` to check file sizes in the config directory:
   ```bash
   ls -la ~/.cli-proxy-api/
   ```
   *Crucial detail:* If you see JSON auth files (e.g., `antigravity-*.json`) that are exactly 0 bytes, the OAuth token was corrupted by an ungraceful shutdown or sudden VPS reboot.

4. **Implement Systemd Graceful Lifecycle**
   To prevent future 0-byte corruption, create a systemd user service using the `terminal` tool:
   ```bash
   mkdir -p ~/.config/systemd/user/
   cat << 'EOF' > ~/.config/systemd/user/cli-proxy-api.service
   [Unit]
   Description=CLIProxyAPI
   After=network-online.target
   Wants=network-online.target

   [Service]
   Type=simple
   WorkingDirectory=/opt/cli-proxy-api
   ExecStart=/opt/cli-proxy-api/cli-proxy-api -config /opt/cli-proxy-api/config.yaml
   Restart=on-failure
   RestartSec=2
   Environment=HOME=/home/USER

   [Install]
   WantedBy=default.target
   EOF
   systemctl --user daemon-reload
   systemctl --user enable --now cli-proxy-api.service
   ```

5. **Prompt User for Re-Authentication**
   Because the auth file is corrupted, the user must manually re-run the OAuth flow in their browser (e.g., clicking a localhost callback link). Wait for them to confirm completion.

6. **Re-link Models to Hermes**
   Once models appear in the `/v1/models` endpoint, configure Hermes. *Note: Hermes prevents the `patch` tool from modifying `~/.hermes/config.yaml` directly due to security guards.*
   Use the `terminal` tool with the Hermes CLI:
   ```bash
   hermes config set custom_providers '[{"name": "cli-proxy-api", "base_url": "http://127.0.0.1:42869/v1", "api_key": "***", "model": "gemini-3-flash"}]'
   ```
   *(Alternatively, instruct the user to use `hermes model` for auto-discovery).*

## Pitfalls
- **Sudden Reboots:** Running `cli-proxy-api` in the background manually (`&` or `nohup`) leaves it vulnerable to SIGKILL on reboot, causing it to truncate auth files to 0 bytes while saving. Always use systemd.
- **Hermes Security Guards:** You cannot use the `patch` tool to edit `~/.hermes/config.yaml`. You must use the `hermes config` CLI commands or `execute_code` if complex string manipulation is strictly necessary.
- **JSON String Parsing in Config:** `hermes config set custom_providers '[...]'` stores the input as a stringified JSON array in the YAML file. Hermes handles this correctly at runtime, but manual YAML editors might be confused. 

## Verification
Run `curl -sS http://127.0.0.1:42869/v1/models` via `terminal` and verify the `data` array contains the expected upstream models, indicating successful authentication and provider routing.
