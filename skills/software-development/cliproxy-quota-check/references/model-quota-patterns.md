# Model Quota Patterns — CLIProxyAPI (antigravity provider)

Discovered during session 2026-07-07. These patterns are specific to the antigravity provider on cloudcode-pa.googleapis.com.

---

## Quota Exhaustion Errors

### `gemini-3-flash` — Individual Quota Exhausted
**Error code:** 429
**Status:** RESOURCE_EXHAUSTED
**Domain:** cloudcode-pa.googleapis.com
**Reason:** QUOTA_EXHAUSTED

```json
{
  "error": {
    "code": 429,
    "message": "Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 42h51m11s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "QUOTA_EXHAUSTED",
        "domain": "cloudcode-pa.googleapis.com",
        "metadata": {
          "uiMessage": "true",
          "model": "gemini-3-flash",
          "quotaResetDelay": "42h51m11.398527173s",
          "quotaResetTimeStamp": "2026-07-09T07:03:05Z"
        }
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "154271.398527173s"
      }
    ]
  }
}
```

**Per-account reset times (observed 2026-07-07):**
| Account | Reset Time (UTC) | Reset In |
|---|---|---|
| mynamenont@gmail.com | 2026-07-09T07:03:05Z | ~42h 51m |
| satang.thevalue@gmail.com | 2026-07-08T15:30:09Z | ~27h 18m |
| thanaphol369@gmail.com | ~2026-07-07T22:12:00Z | ~3h |

---

### `gemini-3.1-pro-low` — Model Cooldown
**Error code:** 429 (different payload)
**Code:** model_cooldown

```json
{
  "error": {
    "code": "model_cooldown",
    "message": "All credentials for model gemini-3.1-pro-low are cooling down via provider antigravity",
    "model": "gemini-3.1-pro-low",
    "provider": "antigravity",
    "reset_seconds": 10788,
    "reset_time": "2h59m48s"
  }
}
```

**Key difference:** This is a **provider-level cooldown** affecting ALL accounts simultaneously, not per-account quota.

---

## False 429 — Disk Full

**Log symptom:**
```
failed to create request body temp file, falling back to direct write error=write /home/thaieasyvps/.cli-proxy-api/logs/request-body-XXXX.tmp: no space left on device
```

**HTTP response:** 429 (but NOT a quota issue)

**Root cause:** Disk at 100% usage (`df -h` shows 44M free on 49G)

**Fix:** Clear `~/.cli-proxy-api/logs/` or other space.

---

## Healthy Model Alternatives (when gemini-3-flash exhausted)

| Model | Tier | Notes |
|---|---|---|
| `gemini-3.5-flash-extra-low` | Extra low | Separate quota, usually available |
| `gemini-3.1-flash-lite` | Lite | Good fallback, fast |
| `gemini-3.5-flash-low` | Low | Balanced |
| `gemini-pro-agent` | Agent | May have separate quota |
| `gemini-3-flash-agent` | Agent separate quota |
| `gemini-3.1-flash-image` | Multimodal | Image generation |
| `claude-sonnet-4-6` | Anthropic | Different provider, separate pool |
| `claude-opus-4-6-thinking` | Anthropic | Different provider |
| `gpt-oss-120b-medium` | Open-weight | Different provider |

---

## Account Health Baselines

| Account | Typical Success Rate | Notes |
|---|---|---|
| mynamenont@gmail.com | ~99% | Healthy |
| thanaphol369@gmail.com | ~99% | Healthy, handles bulk traffic |
| satang.thevalue@gmail.com | ~57% | **Chronic issues** — investigate auth/project limits |

---

## Log Locations

- Error logs: `~/.cli-proxy-api/logs/error-v1-chat-completions-*.log`
- Each request logs full request/response (huge — rotate weekly)
- Search for quota: `grep -l "QUOTA_EXHAUSTED" ~/.cli-proxy-api/logs/*.log`

---

## Quick Diagnostic Commands

```bash
# 1. Account status
curl -H "Authorization: Bearer satangza15974201" http://127.0.0.1:42869/v0/management/auth-files

# 2. Available models
curl -s http://127.0.0.1:42869/v1/models

# 3. Check disk
df -h /home/thaieasyvps

# 4. Recent quota errors
grep -A10 "QUOTA_EXHAUSTED" ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log | head -50

# 5. Service logs
journalctl -u cliproxy -n 50 --no-pager
```