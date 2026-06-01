#!/usr/bin/env bash
set -e
# Helper: generate SSH deploy key for obsidian vault automation
KEY_PATH="$HOME/.ssh/obsidian_vault_deploy"
if [ -f "$KEY_PATH" ]; then
  echo "Key already exists: $KEY_PATH"; exit 0
fi
ssh-keygen -t ed25519 -f "$KEY_PATH" -N "" -C "obsidian-vault-deploy@$(hostname)"
echo "Public key (copy to GitHub Deploy Keys):"
cat "$KEY_PATH.pub"
