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
- **Need to force systemd to pick up new `.env` variables** (e.g. after updating Infisical secrets and syncing them to `~/.hermes/.env`). See `references/troubleshooting_gateway_env_reload.md` for the correct daemon-reload sequence.

## Recovery Playbook (fast path)

1. **Status, then start if dead**
   ```bash
   hermes gateway status
   hermes gateway start
   hermes gateway status
   ```
   If the systemd service is `disabled`, the start is still valid for the current session, but enabling it prevents recurrence after logout/reboot.

2. **Restarting or Enabling Gateway Profiles after Server Reboot**
   If the VPS/Server restarts, any `hermes-gateway-<profile>.service` that was NOT enabled in systemd will remain down (`inactive (dead)`). 
   - **Check status:** `systemctl --user list-units | grep -i hermes` (shows running gateways)
   - **Start the missing profile:** `systemctl --user start hermes-gateway-<profile>.service`
   - **CRITICAL: Ensure it survives the next reboot:** Always run `systemctl --user enable hermes-gateway-<profile>.service` (or hit `Y` to "Start the gateway automatically on login/boot with systemd?" when running `hermes --profile <profile> gateway install`).

3. **Verify platform connections**
   ```bash
   hermes status
   ```
   Look for `telegram connected`, `api_server connected`, etc.

   *Pitfall: Token Already in Use (Cross-Profile Collision)*
   If `hermes status` or logs show `Telegram bot token already in use (PID <PID>). Stop the other gateway first.`:
   - Check `ps aux | grep <PID>` to identify the offending profile or process.
   - Gracefully stop the conflicting profile's gateway: `hermes --profile <profile_name> gateway stop`
   - If zombie processes remain, explicitly kill them: `kill -9 <PID>`
   - Restart the primary gateway.

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

## Cross-Profile Port/Token Conflicts

If `hermes status` or the gateway logs (`tail -n 80 ~/.hermes/logs/gateway.log`) report a startup conflict like:
`Telegram bot token already in use (PID XXX). Stop the other gateway first.`
or
`[Api_Server] Port 8642 already in use.`

This usually means another Hermes profile on the same host is running a gateway service in the background and holding the same platform tokens or API server ports.

### Conflict Recovery:
1. Identify the conflicting profile from `hermes gateway status` under the `Other profiles:` section.
2. Stop and uninstall the conflicting profile's gateway if it shouldn't be running:
   ```bash
   hermes --profile <conflicting-profile> gateway stop
   hermes --profile <conflicting-profile> gateway uninstall
   ```
   (If the uninstaller misses the systemd unit, manually run `rm -f ~/.config/systemd/user/hermes-gateway-<profile>.service && systemctl --user daemon-reload`).
3. Start the primary gateway with `hermes gateway start`.

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
