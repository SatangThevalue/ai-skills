---
name: telegram-polling-conflict-troubleshooting
description: Resolve Telegram bot getUpdates polling conflicts.
version: 0.1.0
metadata:
  hermes:
    tags: [Telegram, Gateway, Troubleshooting, Systemd]
---

# Telegram Polling Conflict Troubleshooting

Diagnoses and resolves Telegram bot polling conflicts where multiple processes poll `getUpdates` using the same bot token. It isolates orphaned background daemons and clears polling locks without restarting active gateway sessions. Relies on standard Linux process management and systemd.

## When to Use
- Telegram bot stops responding or becomes unresponsive to user messages.
- Gateway log reports `Conflict: terminated by other getUpdates request`.
- Multiple scripts or subagents share the same Telegram bot token.

## Prerequisites
- Profile gateway installed and managed under `systemd --user`.
- Profile logs accessible at `~/.hermes/profiles/<profile>/logs/gateway.log` or systemd journal.
- Process management permissions (`ps`, `kill`).

## How to Run
Inspect gateway service status and logs using `read_file` or the `terminal` tool. Terminate competing processes via the `terminal` tool.

## Quick Reference
```bash
systemctl --user status hermes-gateway-<profile>.service --no-pager
tail -n 30 ~/.hermes/profiles/<profile>/logs/gateway.log
ps aux | grep -E "python.*(telegram|bot_daemon)"
kill -9 <PID>
```

## Procedure

1. **Check Service Status and Logs**
   Inspect the systemd service for conflict warnings using the `terminal` tool:
   ```bash
   systemctl --user status hermes-gateway-<profile>.service --no-pager
   ```
   Read the gateway log using `read_file` or `terminal`:
   ```bash
   tail -n 30 ~/.hermes/profiles/<profile>/logs/gateway.log
   ```
   Look for: `Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`.

2. **Identify Competing Bot Processes**
   Locate all processes running Telegram bots or referencing the token/scripts:
   ```bash
   ps aux | grep -E "python.*(telegram|bot_daemon)"
   ```
   Check if an orphaned standalone daemon, background script, or test instance is actively executing.

3. **Terminate Rogue Instance**
   Kill the duplicate process holding the polling lock:
   ```bash
   kill -9 <rogue_pid>
   ```

4. **Wait for Lock Expiration**
   Telegram holds open HTTP long-polling connections for up to 20-30 seconds. Do not trigger a service restart immediately. Allow the gateway polling adapter to automatically resume:
   ```bash
   sleep 10
   tail -n 20 ~/.hermes/profiles/<profile>/logs/gateway.log
   ```
   Confirm the log displays `Telegram polling resumed after conflict retry`.

## Pitfalls
- **In-Session Restart Lock**: Running `systemctl --user restart hermes-gateway` from inside an active Hermes agent turn is blocked by the gateway process manager to prevent abrupt SIGTERM kill of the executing command. Terminate the rogue external process instead of restarting the gateway.
- **Telegram Polling Timeout**: Killing the conflicting process does not release the connection instantly on Telegram's side; wait 20 seconds for the Telegram server session to time out.
- **Token Re-use across Services**: Assign unique bot tokens per service or profile to prevent recurring polling race conditions.

## Verification
Verify that polling is restored and conflict errors have stopped:
```bash
tail -n 15 ~/.hermes/profiles/<profile>/logs/gateway.log | grep -E "Telegram polling resumed|✓ telegram connected" && echo "SUCCESS: Polling active"
```
