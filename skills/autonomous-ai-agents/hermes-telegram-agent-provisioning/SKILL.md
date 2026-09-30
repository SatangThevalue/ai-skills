---
name: hermes-telegram-agent-provisioning
description: Provision an isolated profile as a Telegram daemon.
version: 0.1.0
metadata:
  hermes:
    tags: [Hermes, Telegram, Profiles, Systemd]
---

# Hermes Telegram Agent Provisioning

End-to-end procedure for cloning a Hermes profile into an isolated subagent with custom personality, dedicated Telegram bot credentials, and an autostarting user systemd service. It does not manage shared multiplexer gateways. Relies on Hermes CLI, Python standard library, and systemd.

## When to Use
- User asks to create a new profile with a dedicated Telegram bot.
- Setting up a specialized assistant with custom SOUL.md and Telegram access.
- Deploying a cloned agent persona as an independent background daemon.

## Prerequisites
- Hermes CLI installed and operational in environment.
- Dedicated Telegram bot token from @BotFather.
- Authorized Telegram user ID (numeric string, e.g. "7789252439").
- Systemd user linger enabled (`loginctl enable-linger $USER`).

## How to Run
Invoke provisioning commands via the `terminal` tool or run `scripts/provision.py`. Author personality and memory files using `write_file` with `cross_profile: true`.

## Quick Reference
```bash
hermes profile create <profile> --clone --description "<desc>"
hermes -p <profile> config set gateway.platforms '["telegram"]'
hermes -p <profile> config set gateway.telegram.token '${TELEGRAM_BOT_TOKEN}'
hermes -p <profile> config set gateway.telegram.allowed_users '"<user_id>"'
hermes -p <profile> config set gateway.telegram.reactions true
hermes -p <profile> config set gateway.telegram.extra.rich_messages true
hermes -p <profile> config set gateway.multiplex_profiles false
hermes -p <profile> gateway install
systemctl --user status hermes-gateway-<profile>.service
```

## Procedure

1. **Clone Base Profile**
   Run the profile creation command via the `terminal` tool to copy base configurations, skills, and tools:
   ```bash
   hermes profile create <profile_slug> --clone --description "<description>"
   ```

2. **Configure Custom Personality and Scoped Memories**
   Use `write_file` with `cross_profile: true` to author `~/.hermes/profiles/<profile_slug>/SOUL.md` containing role definitions, behavioral directives, and response structures.
   Update `~/.hermes/profiles/<profile_slug>/memories/USER.md` and `~/.hermes/profiles/<profile_slug>/memories/MEMORY.md` to isolate working memory from other profiles.

3. **Populate Environment Variables**
   Update `~/.hermes/profiles/<profile_slug>/.env` to store secrets with restricted file permissions:
   ```bash
   python3 -c '
   import os, re
   path = os.path.expanduser("~/.hermes/profiles/<profile_slug>/.env")
   with open(path, "r", encoding="utf-8") as f:
       data = f.read()
   data = re.sub(r"TELEGRAM_BOT_TOKEN=.*", "TELEGRAM_BOT_TOKEN=<bot_token>", data)
   data = re.sub(r"TELEGRAM_ALLOWED_USERS=.*", "TELEGRAM_ALLOWED_USERS=<user_id>", data)
   data = re.sub(r"TELEGRAM_HOME_CHANNEL=.*", "TELEGRAM_HOME_CHANNEL=<user_id>", data)
   with open(path, "w", encoding="utf-8") as f:
       f.write(data)
   ' && chmod 600 ~/.hermes/profiles/<profile_slug>/.env
   ```

4. **Set Gateway Configuration**
   Configure Telegram gateway parameters for the profile using the `terminal` tool:
   ```bash
   hermes -p <profile_slug> config set gateway.platforms '["telegram"]'
   hermes -p <profile_slug> config set gateway.telegram.token '${TELEGRAM_BOT_TOKEN}'
   hermes -p <profile_slug> config set gateway.telegram.allowed_users '"<user_id>"'
   hermes -p <profile_slug> config set gateway.telegram.reactions true
   hermes -p <profile_slug> config set gateway.telegram.extra.rich_messages true
   hermes -p <profile_slug> config set gateway.multiplex_profiles false
   ```

5. **Install and Start Systemd Daemon**
   Install the profile gateway as a persistent user service:
   ```bash
   hermes -p <profile_slug> gateway install
   ```
   Ensure systemd linger is enabled so the daemon runs headlessly across sessions:
   ```bash
   loginctl enable-linger $USER
   ```

6. **Verify Gateway Connection**
   Inspect logs using `read_file` on `~/.hermes/profiles/<profile_slug>/logs/gateway.log` to confirm initialization and platform connection.

## Pitfalls
- **Token in config.yaml:** Never place raw bot tokens inside `config.yaml`. Always reference `${TELEGRAM_BOT_TOKEN}` and store the actual secret in `.env`.
- **Multiplexer Collision:** Always set `gateway.multiplex_profiles false` when giving a profile its own independent bot token and systemd daemon.
- **Cross-Profile Guard:** Tool calls modifying files in `~/.hermes/profiles/<profile>/` must pass `cross_profile: true` or the write is rejected.
- **Allowed Users Formatting:** The value passed to `gateway.telegram.allowed_users` must be quoted (e.g. `'"7789252439"'`).
- **Headless Termination:** Without systemd linger, user daemons stop when the SSH session closes.

## Verification
Execute the following verification check via the `terminal` tool:
```bash
systemctl --user is-active hermes-gateway-<profile_slug>.service && \
tail -n 20 ~/.hermes/profiles/<profile_slug>/logs/gateway.log | grep -q "✓ telegram connected" && \
echo "SUCCESS: Gateway active and connected"
```
