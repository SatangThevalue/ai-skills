---
name: hermes-gateway-resilience
description: Restore and harden the Hermes Messaging Gateway on Linux when it goes inactive, drops platform connections, or fails under low-disk pressure.
version: 0.1.0
metadata:
  hermes:
    tags:
      - gateway
      - recovery
      - disk-pressure
      - linux
      - telegram
---

# Hermes Gateway Resilience

Operational recovery patterns for `hermes-gateway.service`. Use when the gateway reports `inactive (dead)`, when connections drop after validator errors, or when background components stop ticking.

## When to Use

- Gateway status shows `inactive (dead)`.
- `hermes status` shows platform `configured` but not `connected` after recent errors.
- Background subsystems (Kanban dispatcher, scheduler) begin failing with storage errors.
- The user explicitly reports "Hermes just stopped talking to me."
- **Need to restart the gateway from inside a gateway session** (e.g. after changing `.env` variables or config.yaml settings).

## Recovery Playbook (fast path)

1. **Status, then start if dead**
   ```bash
   hermes gateway status
   hermes gateway start
   hermes gateway status
   ```
   If the systemd service is `disabled`, the start is still valid for the current session, but enabling it prevents recurrence after logout/reboot.

2. **Verify platform connections**
   ```bash
   hermes status
   ```
   Look for `telegram connected`, `api_server connected`, etc.

3. **Light-touch log triage**
   ```bash
   tail -n 80 ~/.hermes/logs/gateway.log
   ```
   The last 80 lines almost always contain the disconnection signature.

4. **Restarting Gateway from Inside a Session (Internal Handoff)**
   ⚠️ **CRITICAL LIMIT:** You cannot run `hermes gateway restart` or `systemctl --user restart hermes-gateway` directly inside the agent conversation. The gateway process will intercept its own SIGTERM, kill the child shell process, and drop the current execution turn (leading to timeouts or failed execution states).
   
   *Workaround:* Schedule a one-shot `cronjob` (using the `cronjob` tool) to run the restart script slightly in the future (e.g. 30 seconds from now) so the current turn can complete cleanly and release locks before the gateway process terminates and restarts.
   
   *Syntax Example:*
   ```python
   # Schedule restart 30 seconds from current time
   cronjob(
       action="create",
       prompt="systemctl --user restart hermes-gateway",
       schedule="2026-06-28T07:53:10"  # ISO timestamp 30s in the future
   )
   ```

## Low-Disk Resilience

A disk-full condition on the host often surfaces inside SQLite-backed components, not at the filesystem API directly.

### Real failure shape from operator history

```
sqlite3.OperationalError: disk I/O error
```
followed by:
```
Channel directory: failed to write: [Errno 28] No space left on device
```

### Operator actions

- Run `df -h /home /var /tmp ~/.hermes` to confirm the pressure.
- Recover space on the partition backing `~/.hermes/` before restarting components.
- Do not rely solely on restarting Hermes while disk pressure remains; the first write will reproduce the failure and backoff will start again.

### Proactive guidance

If monitoring is in place, alert before the partition drops below 15% available.

## Platform Reconnection Behavior

Reconnectable platforms such as Telegram auto-recover from transient failures and will register as connected again after start. A freshly started gateway regenerates commands and resumes long polling without manual reconfiguration.

## Verification

Treat `hermes gateway status` showing `active (running)` plus platform lines marked `connected` as the diagnostic terminus. If the connection is clean, the user should still verify end-to-end by sending a real inbound message on the target platform.
