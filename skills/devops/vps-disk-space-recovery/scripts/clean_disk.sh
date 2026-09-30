#!/usr/bin/env bash
set -eo pipefail

echo "=== [1/5] Cleaning user package & build caches ==="
rm -rf ~/.npm/_cacache ~/.cache/uv /tmp/ai-skills /tmp/node-compile-cache /tmp/data-gym-cache 2>/dev/null || true
rm -rf ~/.hermes/profiles/*/home/.npm/_cacache 2>/dev/null || true
rm -rf ~/.hermes/cache/videos/* 2>/dev/null || true

if command -v docker >/dev/null 2>&1; then
    echo "=== [2/5] Pruning Docker build layers ==="
    docker builder prune -f 2>/dev/null || true
fi

SUDO_CMD=""
if [ "$(id -u)" -ne 0 ]; then
    if [ -n "$SUDO_ASKPASS" ] || sudo -n true 2>/dev/null; then
        SUDO_CMD="/usr/bin/sudo -A"
    else
        echo "Notice: Non-root execution without SUDO_ASKPASS; skipping system-level vacuuming."
    fi
fi

if [ -n "$SUDO_CMD" ] || [ "$(id -u)" -eq 0 ]; then
    echo "=== [3/5] Vacuuming systemd journal logs to 100M ==="
    $SUDO_CMD journalctl --vacuum-size=100M 2>/dev/null || true

    if command -v snap >/dev/null 2>&1; then
        echo "=== [4/5] Removing disabled snap revisions & enforcing retention ==="
        snap list --all 2>/dev/null | awk '/disabled/{print $1, $3}' | while read -r snapname revision; do
            $SUDO_CMD snap remove "$snapname" --revision="$revision" 2>/dev/null || true
        done
        $SUDO_CMD snap set system refresh.retain=2 2>/dev/null || true
        $SUDO_CMD rm -rf /var/lib/snapd/cache/* 2>/dev/null || true
    fi

    echo "=== [5/5] Truncating oversized rotated logs & apt clean ==="
    $SUDO_CMD truncate -s 0 /var/log/syslog.1 /var/log/btmp /var/log/btmp.1 2>/dev/null || true
    $SUDO_CMD apt-get autoremove -y 2>/dev/null || true
    $SUDO_CMD apt-get clean 2>/dev/null || true
fi

echo "=== Disk space recovery complete ==="
df -h /
