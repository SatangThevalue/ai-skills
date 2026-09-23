---
name: multi-profile-messaging-gateway
description: "Configure and route multiple Hermes profiles within a single Discord/Telegram gateway (Multiplexer)."
version: 0.2.0
---
# Multi-Profile Messaging Gateway (Discord & Telegram)

This skill covers configuring a single Hermes Agent instance to serve multiple profiles across different Discord channels or Telegram chats using the Gateway Multiplexer.

## Core Configuration
1. In the MAIN (default) profile's `config.yaml`, set `gateway.multiplex_profiles: true`.
2. In EACH profile's `config.yaml`, configure the routing (e.g., `gateway.discord.allowed_channels`, `gateway.telegram.allow_users`).
3. **CRITICAL:** Add ALL bot tokens (`DISCORD_TOKEN`, `CRASSULA_TELEGRAM_TOKEN`, etc.) to the **MAIN profile's `.env` file**. The multiplexer runs under the main profile and needs access to all platform tokens to route them.

## ⚠️ Pitfalls
* **Double-Bind / Port Conflict Crash:** Do NOT start individual gateways for each profile (e.g., `systemctl --user start hermes-gateway-bot_trade`). If `multiplex_profiles` is true, starting a separate gateway causes it to crash with `The default gateway is running as a profile multiplexer...`.
* **Fix:** Stop and disable the individual profile gateways. Run `hermes gateway restart` from the main profile. The single multiplexer process handles all profiles automatically.
* **Overriding multiplex_profiles true to an array:** If you change `multiplex_profiles: true` to a specific list (e.g. `multiplex_profiles: '["ton-crassula"]'`), the default profile is excluded from the gateway unless explicitly named in the array. Always use `true` to multiplex all available profiles safely.