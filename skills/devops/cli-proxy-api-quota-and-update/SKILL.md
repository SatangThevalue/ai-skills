---
name: cli-proxy-api-quota-and-update
description: Check CLIProxyAPI account quota and update binary to latest release.
version: 0.1.0
metadata:
  hermes:
    tags: [CLIProxyAPI, Quota, Monitoring, Update, DevOps]
---

# CLIProxyAPI Quota Check and Binary Update

Check account health (success/failure rates) and upgrade the CLIProxyAPI binary to the latest GitHub release. Does NOT manage credentials or modify quotas — read-only monitoring and binary replacement.

## When to Use

- Debugging AI provider failures (429 errors, model cooldowns).
- Auditing request volumes before workloads.
- "Antigravity is no longer supported" error appears.
- Periodic maintenance to keep binary current.

## Prerequisites

- CLIProxyAPI installed at `/opt/cli-proxy-api/cli-proxy-api`.
- Management endpoint enabled on port `42869` with secret `satangza15974201`.
- Systemd service `cliproxy.service` (system-level, not user).
- `wget`, `tar`, `curl`, `sudo` available.

## How to Run

Invoke through the `terminal` tool:

```bash
# Check quota
python3 -c "
import urllib.request, json
req = urllib.request.Request('http://127.0.0.1:42869/v0/management/auth-files', headers={'Authorization': 'Bearer satangza15974201'})
with urllib.request.urlopen(req) as r:
    res = json.loads(r.read().decode())
    for f in res.get('files', []):
        print(f'Account: {f.get(\"account\")} | Provider: {f.get(\"provider\")} | Status: {f.get(\"status\")} | Success: {f.get(\"success\")} | Failed: {f.get(\"failed\")}')
"
```

```bash
# Update binary to latest release
cd /opt/cli-proxy-api && wget -q https://github.com/router-for-me/CLIProxyAPI/releases/download/v7.2.52/CLIProxyAPI_7.2.52_linux_amd64.tar.gz && tar -xzf CLIProxyAPI_7.2.52_linux_amd64.tar.gz && ./cli-proxy-api --version
```

```bash
# Restart service (requires sudo)
sudo systemctl restart cliproxy.service
```

## Quick Reference

| Action | Command |
|--------|---------|
| Quota check | `curl -H "Authorization: Bearer satangza15974201" http://127.0.0.1:42869/v0/management/auth-files` |
| List models | `curl -s http://127.0.0.1:42869/v1/models` |
| Latest release | `curl -s https://api.github.com/repos/router-for-me/CLIProxyAPI/releases/latest \| grep tag_name` |
| Binary path | `/opt/cli-proxy-api/cli-proxy-api` |
| Service name | `cliproxy.service` (system) |
| Config | `/opt/cli-proxy-api/config.yaml` |
| Error logs | `~/.cli-proxy-api/logs/error-v1-chat-completions-*.log` |

## Procedure

1. **Check current version**
   ```bash
   /opt/cli-proxy-api/cli-proxy-api --version
   ```

2. **Query account quota and status**
   ```bash
   python3 -c "
   import urllib.request, json
   req = urllib.request.Request('http://127.0.0.1:42869/v0/management/auth-files', headers={'Authorization': 'Bearer satangza15974201'})
   with urllib.request.urlopen(req) as r:
       res = json.loads(r.read().decode())
       for f in res.get('files', []):
           s = f.get('success', 0); f_ = f.get('failed', 0)
           rate = s/(s+f_)*100 if (s+f_) else 0
           print(f'{f.get(\"account\")} | {f.get(\"provider\")} | {f.get(\"status\")} | {rate:.1f}%')
   "
   ```

3. **Fetch latest release tag**
   ```bash
   curl -s https://api.github.com/repos/router-for-me/CLIProxyAPI/releases/latest | grep '"tag_name"' | cut -d'"' -f4
   ```

4. **Download and extract new binary** (replace `v7.2.52` with actual tag)
   ```bash
   cd /opt/cli-proxy-api
   TAG=v7.2.52
   wget -q https://github.com/router-for-me/CLIProxyAPI/releases/download/${TAG}/CLIProxyAPI_${TAG#v}_linux_amd64.tar.gz
   tar -xzf CLIProxyAPI_${TAG#v}_linux_amd64.tar.gz
   ./cli-proxy-api --version
   ```

5. **Restart systemd service** (requires sudo)
   ```bash
   sudo systemctl restart cliproxy.service
   sleep 3
   ```

6. **Verify service healthy**
   ```bash
   curl -s -H "Authorization: Bearer satangza15974201" http://127.0.0.1:42869/v0/management/auth-files
   ```

## Pitfalls

- **Disk full** — `df -h /` shows 100%: binary download/extract fails silently. Clear space first (`docker system prune -af --volumes`).
- **Service is system-level** — `systemctl --user` will fail with "Unit not found". Use `sudo systemctl`.
- **Sudo password required** — automation needs NOPASSWD or manual entry.
- **Account status `error` with high failure rate** — likely expired/revoked Antigravity auth. Re-login via `-antigravity-login` flag.
- **Binary version flag** — `--version` not defined; use no args or `--help` to see version in output.
- **Config mismatch** — if `remote-management.secret-key` in `config.yaml` doesn't match bearer token, management endpoint returns 401.

## Verification

```bash
# Binary version shows new build date
/opt/cli-proxy-api/cli-proxy-api --version 2>&1 | grep BuiltAt

# Service active and responding
systemctl is-active cliproxy.service && curl -s -H "Authorization: Bearer satangza15974201" http://127.0.0.1:42869/v0/management/auth-files | jq '.files[].status'
```

All accounts should show `"active"` and success rate ≥ 95%.