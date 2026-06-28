---
name: cliproxy-quota-check
description: Check CLIProxyAPI account quota and request success/failure counts.
version: 0.1.0
metadata:
  hermes:
    tags: [API, CLIProxyAPI, Quota, Monitoring, Python]
---

# CLIProxyAPI Quota and Account Status Checker

This skill checks the active status and request quota of CLIProxyAPI accounts by querying the local management endpoint. It reports success/failure counts for debugging and auditing AI model usage.

This skill does NOT manage or modify quotas — it only reads current statistics.

## When to Use

- Debugging why certain AI providers stop responding.
- Auditing daily/weekly request volumes before planning workloads.
- Verifying the CLIProxyAPI service is reachable and healthy.

## Prerequisites

- CLIProxyAPI running locally on port `42869`.
- Management secret configured as `satangza15974201` (or update the script accordingly).

## How to Run

Use `execute_code` to query the management endpoint and parse the JSON response with `json` (stdlib only).

## Quick Reference

- **Management endpoint:** `http://127.0.0.1:42869/v0/management/auth-files`
- **Authorization header:** `Authorization: Bearer satangza15974201`

## Procedure

### 1. Query Account Status and Quota
```python
import urllib.request, json

req = urllib.request.Request(
    'http://127.0.0.1:42869/v0/management/auth-files',
    headers={'Authorization': 'Bearer satangza15974201'}
)

try:
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode())
        for f in res.get('files', []):
            success = f.get('success', 0)
            failed = f.get('failed', 0)
            total = success + failed
            rate = f"{(success/total*100):.1f}%" if total else "N/A"
            print(f"Account: {f.get('account')} | Provider: {f.get('provider')} | Status: {f.get('status')} | Success: {success} | Failed: {failed} | Rate: {rate}")
except Exception as e:
    print('Failed to query CLIProxyAPI:', e)
```

### 2. Interpret Results
| Success Rate | Assessment |
|---|---|
| ≥ 99% | ✅ Healthy — no action needed |
| 95–99% | ⚠️ Monitor — transient network issues |
| < 95% | ❌ Investigate — check provider auth or quota |

A `failed` count in single digits (< 10) against 1,000+ successes is normal and expected.

## Pitfalls

- The management endpoint returns `404` if no `remote-management` secret is configured.
- The endpoint returns `401` if the bearer token does not match.
- High `failed` counts suggest transient network or provider issues.

## Verification

Confirm the connection and parse output successfully:
```python
import urllib.request
req = urllib.request.Request(
    'http://127.0.0.1:42869/v0/management/auth-files',
    headers={'Authorization': 'Bearer satangza15974201'}
)
print('Status code:', urllib.request.urlopen(req).status)