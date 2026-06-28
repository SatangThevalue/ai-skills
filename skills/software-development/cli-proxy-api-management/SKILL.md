---
name: cli-proxy-api-management
description: Configure and query the CLIProxyAPI management endpoints.
version: 0.1.0
metadata:
  hermes:
    tags:
      - API-Gateway
      - Monitoring
      - Configuration
      - Quota
---

# CLIProxyAPI Management and Quota Auditing

This skill covers the configuration and interaction with CLIProxyAPI's management server to audit connected accounts, query quota statuses, and review active requests.

## When to Use
- When configuring `cli-proxy-api` to enable management endpoints.
- When querying active accounts or quota states programmatically.
- When troubleshooting 404 or 401 errors returned by management routes.

## Prerequisites
- CLIProxyAPI installed and running (default port `42869`).
- Python 3 environment.

## How to Run
- Apply configuration updates using the `write_file` or `patch` tools.
- Query API endpoints via `urllib.request` inside the `terminal` tool.

## Quick Reference
- Configuration file: `/opt/cli-proxy-api/config.yaml`
- User auth tokens directory: `~/.cli-proxy-api/`
- List accounts endpoint: `/v0/management/auth-files`
- Request logs endpoint: `/v0/management/logs`
- Get active models list: `GET /v1/models` (requires no auth)

## Systemd User Service Setup
To keep CLIProxyAPI running reliably across system restarts and prevent configuration corruption (empty token files from unexpected SIGKILL):
1. Create a systemd user unit file at `~/.config/systemd/user/cli-proxy-api.service`:
   ```ini
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
   Environment=HOME=/home/thaieasyvps

   [Install]
   WantedBy=default.target
   ```
2. Enable and start the user service:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable cli-proxy-api.service
   systemctl --user start cli-proxy-api.service
   ```

## Procedure

1. **Configure Remote Management**
   Ensure `/opt/cli-proxy-api/config.yaml` has remote management enabled and a secret key set using the `write_file` tool:
   ```yaml
   port: 42869
   remote-management:
     allow-remote: true
     secret-key: "your-management-key"
   ```

2. **Authenticate with Providers (OAuth)**
   If model providers are not configured, you will receive `unknown provider` errors on model completion requests. Perform authentication via device code flows or headless callbacks:
   ```bash
   # Login to Antigravity via Google OAuth
   /opt/cli-proxy-api/cli-proxy-api -antigravity-login
   
   # Verify that the OAuth JSON token file is written successfully
   # to the auth-dir (e.g. ~/.cli-proxy-api/antigravity-<email>.json)
   ```

3. **Verify Models**
   Once logged in, verify models are parsed and available:
   ```bash
   curl -sS http://127.0.0.1:42869/v1/models
   ```

## Pitfalls
- **Default 404 on Management Routes**: By default, if `secret-key` is empty or not configured, all `/v0/management/` routes return `404 Not Found`. You must configure a key to enable these endpoints.
- **Config Corruption on Forceful Shutdowns / Reboots**: If CLIProxyAPI is running as a manual or background process, sudden OS reboots can crash the process mid-write and truncate token files (like `antigravity-<email>.json`) to 0 bytes. Always run CLIProxyAPI via a managed Systemd User Service to ensure graceful shutdowns and state persistence.
- **Timing Safe Verification**: The server uses timing-safe validation. Ensure the key passed exactly matches the `secret-key` value in the YAML file.

## Verification
Verify the management endpoints are reachable and authenticate successfully:
```bash
python3 -c "
import urllib.request
req = urllib.request.Request(
    'http://127.0.0.1:42869/v0/management/config', 
    headers={'Authorization': 'Bearer your-management-key'}
)
print('Connection Status:', urllib.request.urlopen(req).status)
"
```
