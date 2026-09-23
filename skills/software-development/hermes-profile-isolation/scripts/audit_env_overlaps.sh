#!/bin/bash
# Audits Hermes global and profile-specific .env files for overlapping keys
# (e.g., TELEGRAM_BOT_TOKEN vs PROFILE_TELEGRAM_TOKEN) which break Multiplexer routing.

echo "=== Hermes Profile Env Audit ==="
echo "[Global ~/.hermes/.env]"
if [ -f "$HOME/.hermes/.env" ]; then
  grep -E "TOKEN|API_KEY" "$HOME/.hermes/.env"
else
  echo "No global .env found."
fi

echo ""
for d in "$HOME"/.hermes/profiles/*; do
  if [ -d "$d" ] && [ -f "$d/.env" ]; then
    PROFILE=$(basename "$d")
    echo "[$PROFILE ~/.hermes/profiles/$PROFILE/.env]"
    grep -E "TOKEN|API_KEY" "$d/.env"
    echo ""
  fi
done
echo "Check complete. Ensure sub-profiles ONLY have their prefixed tokens in their own .env,"
echo "and their platform polling tokens (if multiplexed) are in the global .env."
