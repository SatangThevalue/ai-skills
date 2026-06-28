---
name: cliproxy-quota-inspector
description: Query and inspect CLIProxyAPI account statuses and request quotas.
version: 0.1.0
metadata:
  hermes:
    tags:
      - API
      - CLIProxyAPI
      - Quota
      - Monitoring
---

# CLIProxyAPI Quota and Account Inspector

This skill allows the agent to interact with the CLIProxyAPI backend (running locally on port `42869`) to retrieve active account lists, check connection statuses, and audit request limits.

## When to Use
- When checking the health or success rate of AI accounts connected to CLIProxyAPI.
- When retrieving active credential configurations to debug request dispatching.
- When auditing daily/weekly quota limits for Codex or Antigravity accounts.

## Prerequisites
- A running CLIProxyAPI instance listening on port `42869` with remote management secret set.
- `satangza15974201` set as the management key.

## How to Run
- Retrieve account statuses using Python scripts invoking the management API through the `terminal` tool.

## Quick Reference
- Get accounts endpoint: `http://127.0.0.1:42869/v0/management/auth-files`
- Authorization header format: `Authorization: Bearer <management-key>`

## Procedure

### 1. Query Active Account List and Quotas
Execute a query to retrieve all configured authentication files, including request counts and operational status:
```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request('http://127.0.0.1:42869/v0/management/auth-files', headers={'Authorization': 'Bearer satangza15974201'})
try:
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode())
        for f in res.get('files', []):
            print(f\"Account: {f.get('account')} | Provider: {f.get('provider')} | Status: {f.get('status')} | Success: {f.get('success')} | Failed: {f.get('failed')}\")
except Exception as e:
    print('Failed to query CLIProxyAPI:', e)
"
```

## Pitfalls
- **404 Not Found**: If `secret-key` is not defined under `remote-management` in `/opt/cli-proxy-api/config.yaml`, the server disables all management endpoints. Verify configuration before querying.
- **401 Unauthorized**: Occurs if the `Authorization: Bearer <key>` header is missing or does not match the configured `secret-key`.

## Verification
Confirm connectivity and verify accounts list retrieval:
```bash
python3 -c "
import urllib.request
req = urllib.request.Request('http://127.0.0.1:42869/v0/management/auth-files', headers={'Authorization': 'Bearer satangza15974201'})
print(urllib.request.urlopen(req).status == 200)
"
```
