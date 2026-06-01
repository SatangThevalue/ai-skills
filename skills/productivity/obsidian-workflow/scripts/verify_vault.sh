#!/usr/bin/env bash
set -e
# Simple verifier for the Obsidian Vault: checks transactions.csv header, runs Python validator, and compares local vs remote HEAD
VAULT="$HOME/Documents/Obsidian Vault"
CRED_FILE="$HOME/.git-credentials-obsidian"
cd "$VAULT"

echo "Running vault verification..."
if [ ! -f transactions.csv ]; then
  echo "ERROR: transactions.csv missing"; exit 2
fi
# check header
head -n1 transactions.csv | grep -q "^id,date,account,counterparty,category,amount_cents" || { echo "ERROR: transactions.csv header mismatch"; exit 3; }
# run python validator if exists
if [ -x scripts/validate_transactions.py ] || [ -f scripts/validate_transactions.py ]; then
  python3 scripts/validate_transactions.py transactions.csv || { echo "Validator failed"; exit 4; }
fi
# compare local vs remote
LOCAL=$(git rev-parse --short HEAD 2>/dev/null || echo "none")
REMOTE=$(git ls-remote origin HEAD | awk '{print substr($1,1,7)}' || echo "none")
echo "local=$LOCAL remote=$REMOTE"
if [ "$LOCAL" = "$REMOTE" ]; then
  echo "OK: local and remote HEAD match"
else
  echo "WARN: local and remote HEAD differ"
fi

echo "Done"
