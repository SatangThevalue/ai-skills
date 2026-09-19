---
name: multi-profile-discord-gateway
description: "Configure and route multiple Hermes profiles within a single Discord server."
version: 0.1.0
metadata:
  hermes:
    tags: [Discord, Multi-Profile, Gateway, Routing, A2A, Infisical]
---

# Multi-Profile Discord Gateway

This skill documents the architecture and setup required to run multiple isolated Hermes profiles (e.g., `bot_trade`, `business`, `developer`) within a single Discord server. It utilizes channel-based routing to ensure each profile only responds in its designated channels, while allowing cross-profile communication via the A2A protocol. Security is maintained by injecting the Discord bot token at runtime via Infisical.

## When to Use
- When the user wants different "personas" or specialized agents in different Discord channels.
- When configuring the Discord gateway for multiple profiles.
- When establishing inter-agent communication (A2A) within a Discord environment.

## Prerequisites
- Hermes profiles created (e.g., `hermes profile create bot_trade --clone`).
- A Discord Bot Token securely stored in Infisical (e.g., `BOT_DISCORD_TOKEN`).
- A Discord server with dedicated channels created and their IDs noted.
- `discord` and `a2a` enabled in the gateway platforms list.

## Quick Reference
- Add platforms: `bot_trade config set gateway.platforms '["discord", "a2a"]'`
- Set allowed channels: `bot_trade config set gateway.discord.allowed_channels '["CHANNEL_ID"]'`
- Run gateway: `infisical run --env=prod --domain <url> -- bot_trade gateway run`

## Procedure

### 1. Profile Creation & Configuration
Ensure all desired profiles are created. Clone from the default profile to inherit base configurations.
```bash
hermes profile create bot_trade --clone --description "Trading Bot"
hermes profile create business --clone --description "Business Manager"
```
Configure each profile's `SOUL.md` to define its specific persona and objectives.

### 2. Enable Discord and A2A
For each profile, ensure both `discord` and `a2a` are enabled in the gateway configuration. A2A allows these isolated profiles to communicate with each other if needed.

```bash
bot_trade config set gateway.platforms '["discord", "a2a"]'
business config set gateway.platforms '["discord", "a2a"]'
```

### 3. Channel Routing (Isolation)
To prevent all bots from replying to every message, strictly bind each profile to specific Discord channel IDs. Use the `allowed_channels` and `free_response_channels` settings.

```bash
# Example for bot_trade
bot_trade config set gateway.discord.allowed_channels "1286311652431528006"
bot_trade config set gateway.discord.free_response_channels "1286311652431528006"
```

### 4. Secure Gateway Execution Script
Create a shell script (`discord_router.sh`) to launch all gateways securely. The script must retrieve the `BOT_DISCORD_TOKEN` from Infisical and pass it to each profile's gateway process. *Do not use shell background wrappers (`nohup`, `&`) within interactive agent sessions.*

```bash
#!/bin/bash
# discord_router.sh

# 1. Retrieve the Discord Token from Infisical securely
export DISCORD_TOKEN=$(infisical run --env=prod --domain http://100.115.66.121:8080 -- printenv BOT_DISCORD_TOKEN)

if [ -z "$DISCORD_TOKEN" ]; then
    echo "❌ ERROR: Failed to retrieve Discord Token."
    exit 1
fi

# 2. Stop existing gateways
hermes gateway stop 2>/dev/null
bot_trade gateway stop 2>/dev/null
business gateway stop 2>/dev/null

# 3. Start gateways as background services (Hermes native method)
# Install the services first (run once)
# bot_trade gateway install
# business gateway install

# CRITICAL SECURITY NOTE: To adhere to Zero-Trust, you must modify the installed 
# systemd service files (e.g., ~/.config/systemd/user/hermes-gateway-bot_trade.service) 
# and prepend `infisical run --env=prod --domain <url> --` to the ExecStart line 
# BEFORE calling systemctl restart. Do not echo secrets into .env files.

echo "Starting services..."
systemctl --user daemon-reload
systemctl --user restart hermes-gateway-bot_trade
systemctl --user restart hermes-gateway-business

echo "✅ All profiles active."
```

## Pitfalls
- **Token Leaks:** Never hardcode the `DISCORD_TOKEN` in the router script or `.env` files. Always extract it at runtime using `infisical run`.
- **Systemd Environment Isolation:** When automating gateway restarts via a bash script (`systemctl restart`), variables exported in the script (like `DISCORD_TOKEN`) are ignored by the systemd daemon. You must modify the `.service` file's `ExecStart` line to wrap the python process with `infisical run`.
- **Channel Overlap:** If `allowed_channels` is left blank, the bot will respond in all channels the Discord role has access to, leading to multiple profiles answering the same prompt simultaneously.
- **Message Content Intent:** The Discord bot will remain silent and ignore messages if the "Message Content Intent" is not enabled in the Discord Developer Portal under the bot's settings.
- **Background Execution:** Do not use `nohup` or trailing `&` when starting gateways from within an active Hermes interactive session, as the parent session cannot track the background processes. Use `gateway install` and `gateway start` for proper daemonization.

## Verification
Send a message in the designated `#trade-signals` Discord channel. Only the `bot_trade` profile should respond, adopting the persona defined in its `SOUL.md`.