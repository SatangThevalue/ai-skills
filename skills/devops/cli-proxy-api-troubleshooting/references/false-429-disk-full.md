# False 429 Errors from Disk Exhaustion

Discovered: 2026-07-07

---

## Symptom

CLIProxyAPI returns **HTTP 429** on all `/v1/chat/completions` requests, but the error response contains **no `quotaResetTimeStamp`** and the logs show:

```
failed to create request body temp file, falling back to direct write error=write /home/thaieasyvps/.cli-proxy-api/logs/request-body-*.tmp: no space left on device
```

This mimics quota exhaustion but is actually **disk full**.

---

## Root Cause

1. CLIProxyAPI writes each request body to a temp file in `~/.cli-proxy-api/logs/` before forwarding
2. When disk hits 100%, temp file creation fails
3. Service falls back to direct write but **still returns 429** (bug/design in request_logger.go:640)
4. User sees "quota exhausted" but it's infrastructure failure

---

## Diagnostic Checklist

```bash
# 1. Check disk immediately when seeing 429
df -h /home/thaieasyvps

# 2. Look for "no space left on device" in logs
grep -r "no space left on device" ~/.cli-proxy-api/logs/

# 3. Verify: real quota errors include quotaResetTimeStamp
#    Disk errors do NOT include quotaResetTimeStamp
```

---

## Quick Fix

```bash
# Clear error logs (largest files)
rm -f ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log

# Vacuum journal
journalctl --vacuum-time=7d

# Verify recovery
curl -sS http://127.0.0.1:42869/v1/chat/completions -X POST -H "Content-Type: application/json" -d '{"model":"gemini-3.5-flash-extra-low","messages":[{"role":"user","content":"test"}]}'
```

---

## Prevention

Add to systemd service or cron:
```bash
# Weekly log rotation
0 3 * * 0 rm -f ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log
```

---

## Related Patterns

See also: `cliproxy-quota-check/references/model-quota-patterns.md` for real quota vs false 429 comparison table.