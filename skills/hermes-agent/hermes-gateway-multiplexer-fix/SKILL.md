---
name: hermes-gateway-multiplexer-fix
description: Fixes Hermes Gateway conflicts when multiplexing profiles.
version: 0.1.0
metadata.hermes.tags:
  - Hermes
  - Gateway
  - Multiplexer
  - Troubleshooting
---

# Hermes Gateway Multiplexer Fix

Resolves auto-restart crash loops and unresponsive bots caused by Hermes Gateway profile conflicts. When the default gateway is set to multiplex profiles, starting a dedicated gateway for a specific profile causes a double-bind conflict (e.g., Telegram polling locks), leading to `status=1/FAILURE`.

## When to Use

- A newly created Hermes profile's gateway is stuck in an auto-restart loop.
- Systemd logs show: "The default gateway is running as a profile multiplexer and already serves profile..."
- A bot (e.g., Telegram) is not responding despite the profile being properly configured.

## Prerequisites

- Access to the host terminal via the `terminal` tool.
- User-level systemd enabled (`systemctl --user`).

## How to Run

Invoke diagnostic commands and systemctl fixes via the `terminal` tool. For the final gateway restart, instruct the user to run it manually to avoid the agent killing its own process.

## Quick Reference

- Check profile logs: `journalctl --user -u hermes-gateway-<profile>.service -n 50 --no-pager`
- Check default logs: `journalctl --user -u hermes-gateway.service -n 50 --no-pager`
- Stop profile service: `systemctl --user stop hermes-gateway-<profile>.service`

## Procedure

1. **Diagnose the Crash Loop**
   Use `terminal` to check the crashing profile's logs:
   ```bash
   journalctl --user -u hermes-gateway-<profile_name>.service -n 50 --no-pager
   ```
   Look for the error: `The default gateway is running as a profile multiplexer and already serves profile...`

2. **Stop and Disable the Redundant Service**
   Disable the profile-specific gateway so it stops fighting the multiplexer for port bindings and webhook/polling locks:
   ```bash
   systemctl --user stop hermes-gateway-<profile_name>.service
   systemctl --user disable hermes-gateway-<profile_name>.service
   ```

3. **Enable the Multiplexer to Route All Profiles**
   If you replace `true` with an explicit JSON array (e.g., `["ton-crassula"]`), the **default profile itself will drop out of the multiplexer**, and routing may break. Ensure the value is `true` (boolean) to catch all active profiles:
   ```bash
   hermes config set gateway.multiplex_profiles true --type json
   ```

4. **Delete Stuck Telegram Webhooks (Crucial for Polling)**
   If a Telegram bot was previously configured with a webhook, polling (`streaming: true`) will silently fail to receive messages. Delete the webhook before restarting the gateway:
   ```bash
   source ~/.hermes/profiles/<profile_name>/.env
   curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook"
   ```

5. **Hard-Restart the Default Gateway (User Action Required)**
   Instruct the user to run these restart commands in their external terminal. **Do not run this via the `terminal` tool if you are currently running inside the gateway, as it will kill your process.** A hard stop/start is required to clear webhook caches:
   ```bash
   systemctl --user stop hermes-gateway
   sleep 2
   systemctl --user start hermes-gateway
   ```

## Pitfalls

- **JSON True vs Array:** Setting `gateway.multiplex_profiles` to `["profile"]` explicitly locks out the default profile. Use `true --type json` to safely multiplex everything.
- **Telegram Webhook Conflict:** If inbound messages are ignored but outbound works, a stale webhook is blocking polling. Always clear it via `deleteWebhook` API call.
- **Self-Termination:** Running `systemctl --user restart hermes-gateway` from inside an agent tool call will be blocked. Always ask the user to execute it.

## Verification

Run `hermes gateway status` via `terminal` to confirm the default gateway is active, then use `hermes -p <profile_name> send --to telegram:<chat_id> "Test message"` to verify outbound connectivity, and ask the user to reply to verify inbound polling.
