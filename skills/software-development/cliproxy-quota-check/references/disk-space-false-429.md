# Disk Space Root Cause — CLIProxyAPI False 429 Errors

Discovered: 2026-07-07

---

## The Problem

When disk is at 100% usage, CLIProxyAPI returns **HTTP 429** with error messages that look like quota exhaustion, but are actually **disk full** errors.

### Log Evidence

```
[2026-07-07 18:08:04] [--------] [warn ] [request_logger.go:640] failed to create request body temp file, falling back to direct write error=write /home/thaieasyvps/.cli-proxy-api/logs/request-body-2238033846.tmp: no space left on device
[2026-07-07 18:08:04] [e1187942] [warn ] [gin_logger.go:100] 429 |        6.789s |       127.0.0.1 | POST    "/v1/chat/completions"
```

**Pattern:** `no space left on device` in request_logger.go → immediate 429 response

---

## Root Cause

- CLIProxyAPI writes request bodies to temp files in `~/.cli-proxy-api/logs/` before forwarding upstream
- When disk is full, temp file creation fails
- Service falls back to direct write but still returns 429
- **This mimics quota exhaustion but is infrastructure failure**

---

## Diagnosis

```bash
# Check disk usage
df -h /home/thaieasyvps

# Output showing problem:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda3        49G   46G   44M 100% /
```

**Threshold:** < 100MB free = imminent failure

---

## Quick Fix

```bash
# Clear CLIProxyAPI error logs (biggest culprit)
rm -f ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log

# Clear journal logs (if large)
journalctl --vacuum-time=7d

# Check what's using space
du -sh /home/thaieasyvps/* | sort -hr | head -20
```

---

## Prevention

1. **Add cron job** to rotate logs weekly:
   ```bash
   # In hermes cronjob
   0 3 * * 0 rm -f ~/.cli-proxy-api/logs/error-v1-chat-completions-*.log
   ```

2. **Monitor disk** in health checks:
   ```bash
   # Alert if < 500MB free
   df -h / | awk 'NR==2 {gsub("%","",$5); if ($5 > 95) print "DISK CRITICAL"}'
   ```

3. **Configure log rotation** in CLIProxyAPI config (if supported)

---

## Key Distinction

| Symptom | Real Quota Exhausted | Disk Full (False 429) |
|---|---|---|
| Error message | "Individual quota reached" | "no space left on device" in logs |
| `quotaResetTimeStamp` | Present in response | **Absent** |
| All models affected | No (model-specific) | Yes (all requests) |
| `df -h` shows | Normal | 100% used |
| Fix | Wait / switch model | Clear disk space |

---

## This Session's Resolution

- Disk was at 44M free (100% used)
- Cleared error logs → freed space
- Service recovered without model switching
- `satang.thevalue@gmail.com` low success rate (57%) was **unrelated** — separate auth/project issue