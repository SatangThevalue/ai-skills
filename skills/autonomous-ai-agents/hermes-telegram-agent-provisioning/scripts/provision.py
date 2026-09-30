#!/usr/bin/env python3
"""Automated provisioning helper for Hermes Telegram agent profiles."""

import argparse
import os
import re
import subprocess
import sys


def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and res.returncode != 0:
        print(f"Error running command: {cmd}\n{res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    return res.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Provision an isolated Hermes Telegram agent profile")
    parser.add_argument("--profile", required=True, help="Profile slug (lowercase, alphanumeric)")
    parser.add_argument("--token", required=True, help="Telegram bot token from @BotFather")
    parser.add_argument("--user-id", required=True, help="Authorized Telegram user ID")
    parser.add_argument("--desc", default="Dedicated Telegram agent profile", help="Profile description")
    args = parser.parse_args()

    slug = args.profile
    token = args.token
    user_id = args.user_id
    desc = args.desc

    print(f"[*] Creating Hermes profile: {slug}...")
    run_cmd(f'hermes profile create {slug} --clone --description "{desc}"')

    env_path = os.path.expanduser(f"~/.hermes/profiles/{slug}/.env")
    if os.path.exists(env_path):
        print(f"[*] Configuring environment variables in {env_path}...")
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "TELEGRAM_BOT_TOKEN=" in content:
            content = re.sub(r"TELEGRAM_BOT_TOKEN=.*", f"TELEGRAM_BOT_TOKEN={token}", content)
        else:
            content += f"\nTELEGRAM_BOT_TOKEN={token}\n"

        if "TELEGRAM_ALLOWED_USERS=" in content:
            content = re.sub(r"TELEGRAM_ALLOWED_USERS=.*", f"TELEGRAM_ALLOWED_USERS={user_id}", content)
        else:
            content += f"\nTELEGRAM_ALLOWED_USERS={user_id}\n"

        if "TELEGRAM_HOME_CHANNEL=" in content:
            content = re.sub(r"TELEGRAM_HOME_CHANNEL=.*", f"TELEGRAM_HOME_CHANNEL={user_id}", content)
        else:
            content += f"\nTELEGRAM_HOME_CHANNEL={user_id}\n"

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.chmod(env_path, 0o600)

    print("[*] Setting gateway configuration keys...")
    run_cmd(f"hermes -p {slug} config set gateway.platforms '[\"telegram\"]'")
    run_cmd(f"hermes -p {slug} config set gateway.telegram.token '${{TELEGRAM_BOT_TOKEN}}'")
    run_cmd(f'hermes -p {slug} config set gateway.telegram.allowed_users \'"{user_id}"\'')
    run_cmd(f"hermes -p {slug} config set gateway.telegram.reactions true")
    run_cmd(f"hermes -p {slug} config set gateway.telegram.extra.rich_messages true")
    run_cmd(f"hermes -p {slug} config set gateway.multiplex_profiles false")

    print("[*] Installing and enabling systemd user service...")
    run_cmd(f"hermes -p {slug} gateway install")

    print(f"[+] Provisioning completed for profile: {slug}")


if __name__ == "__main__":
    main()
