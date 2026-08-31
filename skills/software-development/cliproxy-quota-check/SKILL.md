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

Use `terminal` and `curl` to query the management endpoint and process with `jq` or parse the JSON response manually.

## Quick Reference

- **Management endpoint:** `http://127.0.0.1:42869/v0/management/auth-files`
- **Authorization header:** `Authorization: Bearer satangza15974201`
- **Models endpoint:** `http://127.0.0.1:42869/v1/models` (lists available models per provider)
- **Error logs:** `~/.cli-proxy-api/logs/error-v1-chat-completions-*.log`

## Procedure

### 1. Query Account Status and Quota
```bash
curl -H "Authorization: Bearer satangza15974201" http://127.0.0.1:42869/v0/management/auth-files
```

### 2. List Available Models
```bash
curl -s http://127.0.0.1:42869/v1/models
```

### 3. Interpret Results — Account Level
| Success Rate | Assessment |
|---|---|
| ≥ 99% | ✅ Healthy — no action needed |
| 95–99% | ⚠️ Monitor — transient network issues |
| < 95% | ❌ Investigate — check provider auth or quota |

A `failed` count in single digits (< 10) against 1,000+ successes is normal and expected.

### 4. Interpret Results — Model Level (Critical)
When a model returns `429 QUOTA_EXHAUSTED`, check the error logs for per-account reset timestamps:

```bash
cat ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log | grep -A5 "QUOTA_EXHAUSTED"
```

Key fields in the error response:
- `quotaResetTimeStamp` — exact reset time (UTC)
- `model` — which model is exhausted
- `domain: cloudcode-pa.googleapis.com` — indicates Google Cloud Code API quota

**Common model states:**
| Model | Typical State | Notes |
|---|---|---|
| `gemini-3-flash` | Often exhausted | High demand, per-account daily quota |
| `gemini-3.1-pro-low` | Cooldown periods | `model_cooldown` error, 2-3h reset |
| `gemini-3.5-flash-extra-low` | Usually available | Lower tier, separate quota |
| `gemini-3.1-flash-lite` | Usually available | Good fallback |
| `claude-*` | Different provider | Separate quota pool |

### 5. Check Disk Space (Root Cause of False 429s)
```bash
df -h /home/thaieasyvps
```
If disk is near 100% full, the service cannot write request temp files and returns `429` with `no space left on device` in logs — **not a real quota issue**. Use standard prune commands (`docker system prune -a -f`, `journalctl --vacuum-time=1d`) to recover space.

## Troubleshooting

- **Quota exhausted (`429 QUOTA_EXHAUSTED`)**: Check error logs for `quotaResetTimeStamp`. Switch to alternative model (`gemini-3.5-flash-extra-low`, `gemini-3.1-flash-lite`, `claude-sonnet-4-6`).
- **Model cooldown (`429 model_cooldown`)**: All credentials for that model are cooling down. Wait for `reset_seconds` or switch models.
- **Disk full (false 429)**: `df -h` shows 100% usage. Clear logs in `~/.cli-proxy-api/logs/` or other space.
- **Management endpoint `404`**: No `remote-management` secret configured in `/opt/cli-proxy-api/config.yaml`.
- **Management endpoint `401`**: Bearer token does not match `secret-key` in config (bcrypt hash).
- **High `failed` counts**: Transient network or provider issues. Check recent error logs.
- **"This version of Antigravity is no longer supported"**: Update CLIProxyAPI binary to latest version (v7.2.52+). The antigravity provider requires a minimum CLIProxyAPI version to work with Google's API changes.
  - Check current version: `/opt/cli-proxy-api/cli-proxy-api --version`
  - Latest releases: https://github.com/router-for-me/CLIProxyAPI/releases
  - After binary update, restart the service (system service requires `sudo systemctl restart cliproxy.service`)

## Service Management

- **Service type**: System service (`cliproxy.service`), not user service
- **Binary location**: `/opt/cli-proxy-api/cli-proxy-api`
- **Config**: `/opt/cli-proxy-api/config.yaml`
- **Restart command**: `sudo systemctl restart cliproxy.service`
- **Status check**: `systemctl status cliproxy.service`
- **Logs**: `journalctl -u cliproxy.service -f`

## Pitfalls

- **Account-level success rate ≠ model-level availability** — An account can show 99% success but have `gemini-3-flash` fully exhausted while other models work.
- **`satang.thevalue@gmail.com`** historically shows ~57% success rate — investigate auth freshness or project-specific limits.
- **Error logs accumulate fast** — Rotate or clear `~/.cli-proxy-api/logs/` weekly to prevent disk exhaustion.
- **`quotaResetTimeStamp` is in UTC** — Convert to local (Asia/Bangkok = UTC+7) for scheduling.

## Verification

Confirm the connection and parse output successfully:
```python
import urllib.request
req = urllib.request.Request(
    'http://127.0.0.1:42869/v0/management/auth-files',
    headers={'Authorization': 'Bearer satangza15974201'}
)
print('Status code:', urllib.request.urlopen(req).status)