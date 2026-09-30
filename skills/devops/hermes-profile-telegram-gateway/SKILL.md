---
name: hermes-profile-telegram-gateway
description: Configure and verify Telegram gateway for a named Hermes profile.
version: 0.1.0
metadata:
  hermes:
    tags: [Hermes, Telegram, Gateway, Profiles, Systemd]
    related_skills: [hermes-agent, hermes-profile-customization]
---

# Hermes Profile Telegram Gateway Setup

Connect a specific Hermes profile to its own Telegram bot with user allowlist,
then verify the gateway runs as a persistent systemd service that survives reboots.
Does NOT cover multiplexer mode (one gateway, multiple profiles sharing one bot token).
Requires a dedicated bot token per profile — get one from @BotFather.

## When to Use

- Setting up a new Hermes profile with its own dedicated Telegram bot
- Telegram token changed and gateway needs reconfiguring
- Verifying a profile's gateway survives server reboot
- Restricting a bot to respond only to specific Telegram user IDs

## Prerequisites

- Hermes installed, profile already created (`hermes profile list`)
- Telegram bot token from @BotFather (format: `123456789:AAF...`)
- Telegram user ID(s) to whitelist (get from @userinfobot)
- `systemd --user` available (`loginctl enable-linger $USER` if on headless VPS)

## How to Run

All config commands run via the `terminal` tool using `hermes -p <profile>` prefix.
Gateway status and logs checked via `terminal` tool or `read_file` on the log file.

## Quick Reference

```
hermes -p <profile> gateway status
hermes -p <profile> config set gateway.platforms '["telegram"]'
hermes -p <profile> config set gateway.telegram.token '${TELEGRAM_BOT_TOKEN}'
hermes -p <profile> config set gateway.telegram.allowed_users '"<user_id>"'
hermes -p <profile> config set gateway.telegram.reactions true
hermes -p <profile> config set gateway.telegram.extra.rich_messages true
systemctl --user is-enabled hermes-gateway-<profile>.service
systemctl --user list-units 'hermes*' --no-pager
tail -30 ~/.hermes/profiles/<profile>/logs/gateway.log
```

## Procedure

### 1. Check existing gateway state

```bash
hermes -p <profile> gateway status
```

Note the PID. If already running from a previous session, it may be using stale config — must restart after reconfiguring.

### 2. Verify .env has the token

```bash
cat ~/.hermes/profiles/<profile>/.env | grep -i telegram
```

If `TELEGRAM_BOT_TOKEN` is missing, add it:

```bash
echo "TELEGRAM_BOT_TOKEN=<token>" >> ~/.hermes/profiles/<profile>/.env
chmod 600 ~/.hermes/profiles/<profile>/.env
```

DO NOT hardcode the token directly in config.yaml — always reference via `${TELEGRAM_BOT_TOKEN}`.

### 3. Set gateway config via hermes CLI

Run each line via the `terminal` tool:

```bash
hermes -p <profile> config set gateway.platforms '["telegram"]'
hermes -p <profile> config set gateway.telegram.token '${TELEGRAM_BOT_TOKEN}'
hermes -p <profile> config set gateway.telegram.allowed_users '"<telegram_user_id>"'
hermes -p <profile> config set gateway.telegram.reactions true
hermes -p <profile> config set gateway.telegram.extra.rich_messages true
```

For multiple allowed users:
```bash
hermes -p <profile> config set gateway.telegram.allowed_users '"id1,id2"'
```

Note: `--type json` flag does NOT exist in this hermes version — omit it.

### 4. Verify config was written

```bash
grep -n 'TELEGRAM\|allowed_users\|platforms\|token' \
  ~/.hermes/profiles/<profile>/config.yaml
```

Expect lines showing `token: ${TELEGRAM_BOT_TOKEN}` and `allowed_users` under the `gateway:` block (near end of file, NOT under the `display.platforms` section at line ~332).

### 5. Restart the gateway

Kill the old PID first (cannot restart from inside an active gateway session):

```bash
kill <old_pid>
sleep 2
```

Then start in background via `terminal(background=True)`:

```bash
hermes -p <profile> gateway run
```

Wait 5 seconds, then verify:

```bash
hermes -p <profile> gateway status
```

### 6. Confirm Telegram connected

```bash
tail -30 ~/.hermes/profiles/<profile>/logs/gateway.log
```

Look for:
```
✓ telegram connected
Gateway running with 1 platform(s)
```

### 7. Install as systemd service (survive reboot)

Run from a terminal OUTSIDE the active gateway session:

```bash
hermes -p <profile> gateway install
```

Then verify:

```bash
systemctl --user is-enabled hermes-gateway-<profile>.service
systemctl --user list-units 'hermes*' --no-pager
```

Expected output: `enabled` and `active running`.

## Pitfalls

- **`--type json` flag**: Not supported in this hermes version — omit entirely. Use plain `true`/`false` strings.
- **Config written to wrong section**: `hermes config set gateway.telegram.*` writes near end of file. The `display.platforms.telegram` section at line ~332 is unrelated — confirm with `grep -n`.
- **Token in config.yaml directly**: Always use `${TELEGRAM_BOT_TOKEN}` (env var reference), never paste raw token — secret redaction strips it from logs but it stays in plaintext YAML.
- **Restart from inside gateway session**: `hermes gateway restart` will kill the agent mid-execution. Always kill PID manually then `hermes gateway run` from a separate terminal or background=True.
- **multiplex_profiles: false**: When each profile has its own bot token, DO NOT use multiplexer mode. Each profile needs its own gateway process on its own port/PID.
- **`allowed_users` format**: Must be a quoted string `'"7789252439"'` not a bare integer — hermes config set treats unquoted numbers as strings anyway but quoting prevents ambiguity.
- **Linger not enabled**: On headless VPS, user services die on logout. Fix: `sudo loginctl enable-linger $USER`.
- **Cloned profile .env token conflict**: When creating a profile via `hermes profile create <name> --clone`, `.env` inherits the source profile's `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, and `TELEGRAM_HOME_CHANNEL`. You MUST replace these lines in `~/.hermes/profiles/<name>/.env` before launching the gateway to prevent two bots colliding or running with the wrong identity.
- **`gateway install` prompts**: `hermes -p <profile> gateway install` asks confirmation prompts to start now and auto-start on boot. In scripts or automated pipelines, provide `yes '' | hermes -p <profile> gateway install` or accept defaults.

## Verification

```bash
systemctl --user is-enabled hermes-gateway-<profile>.service \
  && tail -5 ~/.hermes/profiles/<profile>/logs/gateway.log \
  | grep -q "telegram connected" && echo "OK: gateway live and persistent" \
  || echo "FAIL: check log above"
```

Send a test message to the bot from the whitelisted Telegram account — should get a response within 5 seconds.
