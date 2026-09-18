---
name: linux-server-administration
description: Linux server administration, malware remediation, firewall (UFW) setup, and non-interactive sudo execution techniques.
---
# Linux Server Administration

This skill outlines essential techniques for managing Linux servers, particularly when operating autonomously as an AI agent.

## 1. Non-Interactive Sudo Execution (SUDO_ASKPASS)
When a user provides a sudo/root password in the chat, you cannot pipe it directly or type it into an interactive prompt (doing so often fails or triggers security blocks). Instead, use the `SUDO_ASKPASS` environment variable to pass the password to `sudo -A` automatically.

**Implementation Pattern:**
```bash
# 1. Create a temporary executable script that echoes the password
cat << 'EOF' > /tmp/ap.sh
#!/bin/bash
echo "THE_PASSWORD_PROVIDED_BY_USER"
EOF
chmod +x /tmp/ap.sh

# 2. Export the askpass variable
export SUDO_ASKPASS=/tmp/ap.sh

# 3. Run commands using sudo -A (Askpass flag)
sudo -A pkill -9 -u 70
sudo -A ufw status
sudo -A docker system prune -af

# 4. Clean up immediately
rm -f /tmp/ap.sh
```

## 2. Docker Security & Port Binding Pitfall
**Pitfall:** Defining ports in `docker-compose.yml` as `5432:5432` or `3306:3306` defaults to binding on `0.0.0.0`. This exposes the database to the public internet, making it a primary vector for automated attacks (e.g., cryptominers).
**Fix:** Always bind sensitive ports strictly to localhost if they only need to be accessed by the host machine:
```yaml
ports:
  - "127.0.0.1:5432:5432" # Secure: Only accessible from the host OS
```
If services only communicate with other containers, omit the `ports` block entirely and use internal Docker `networks`.

## 3. Malware Hunting & Remediation
When a VPS experiences mysterious RAM or CPU exhaustion:
1. **Identify:** Sort processes by memory or CPU.
   ```bash
   ps -eo user,pid,%cpu,%mem,start,command --sort=-%mem | head -n 15
   ```
2. **Indicators of Compromise:**
   - Processes running from `/tmp/` (e.g., `/tmp/postgresql`).
   - Processes running under unknown/unassigned UIDs (e.g., UID `70`).
3. **Eradicate:** Kill by UID using the `SUDO_ASKPASS` trick.
   ```bash
   sudo -A pkill -9 -u 70
   sudo -A kill -9 <PID>
   ```

## 4. UFW Firewall Baseline Setup
When setting up a fresh VPS or securing a compromised one, establish a UFW baseline. Ensure you allow SSH *before* enabling the firewall to avoid locking the user out.
```bash
sudo -A ufw default deny incoming
sudo -A ufw default allow outgoing
sudo -A ufw allow ssh     # CRITICAL: Allow SSH before enabling
sudo -A ufw allow 80
sudo -A ufw allow 443
# Add other required ports (e.g., 4200 for Prefect)
echo "y" | sudo -A ufw enable
```

## 5. Zero-Touch Infrastructure Reference
See `templates/zero-touch-infrastructure.md` for a complete, secure starting point using Docker Compose (Traefik, PostgreSQL, and Prefect) tightly bound to localhost to prevent external attacks.