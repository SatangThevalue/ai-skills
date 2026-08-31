# Antigravity "Version No Longer Supported" Error

## Error Message
```
This version of Antigravity is no longer supported. Please upgrade to receive the latest features.
```

## Root Cause
Google's Antigravity API (used by CLIProxyAPI for Gemini models) periodically updates its protocol/requirements. Older CLIProxyAPI binaries become incompatible and return this error for all Antigravity accounts.

## Affected Accounts
- Only affects **Antigravity** provider accounts
- Other providers (Codex, Claude, Kimi, xAI, Vertex) are unaffected
- Account status shows as `error` instead of `active`
- Success rate drops dramatically (e.g., ~54% vs 98%+)

## Fix: Update CLIProxyAPI Binary

### 1. Check Current Version
```bash
/opt/cli-proxy-api/cli-proxy-api --version
```

### 2. Download Latest Release
```bash
cd /opt/cli-proxy-api
wget https://github.com/router-for-me/CLIProxyAPI/releases/download/v7.2.52/CLIProxyAPI_7.2.52_linux_amd64.tar.gz
tar -xzf CLIProxyAPI_7.2.52_linux_amd64.tar.gz
```

### 3. Restart Service (System Service)
```bash
sudo systemctl restart cliproxy.service
```

### 4. Verify
```bash
curl -s -H "Authorization: Bearer <management-key>" http://127.0.0.1:42869/v0/management/auth-files
```

## Notes
- CLIProxyAPI releases frequently (daily/weekly) — check GitHub releases regularly
- Disk space must be available for download/extract (~50MB)
- Service is a **system service** (not user service) — requires sudo
- Config file at `/opt/cli-proxy-api/config.yaml` is preserved
- Auth files in `~/.cli-proxy-api/` are preserved

## Related GitHub
- Releases: https://github.com/router-for-me/CLIProxyAPI/releases
- Issue tracker: https://github.com/router-for-me/CLIProxyAPI/issues