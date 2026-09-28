---
name: linux-security-hardening
description: Hardening Linux VPS environments, securing Docker ports, configuring UFW, and responding to rogue/malware processes.
---

# Linux Security Hardening & Incident Response

## Triggers
- Unexplained high RAM/CPU usage on a Linux server.
- Suspicious processes running in `/tmp/` or under unknown UIDs (e.g., Cryptominers/Botnets).
- Securing a newly provisioned VPS, locking down Docker environments, or configuring firewalls.

## 1. Hunting & Terminating Rogue Processes
- **Detect resource hogs:** `ps -eo user,pid,%cpu,%mem,start,command --sort=-%cpu | head -n 20`
- **Check failing/looping services:** Often high CPU spikes are caused by systemd user services stuck in crash loops (e.g. status 203/EXEC or duplicate process collisions):
  ```bash
  systemctl --user list-units --type=service --state=activating,failed
  # Immediately halt and unregister runaway looping services:
  systemctl --user disable --now <service_name>.service
  ```
- **Audit established outbound sockets:** Verify active external connections are benign cloud endpoints (Telegram, Cloudflare, Tailscale):
  ```bash
  python3 -c "import socket, struct; [print(f'{socket.inet_ntoa(struct.pack(\"<L\", int(p[1].split(\":\")[0], 16)))}:{int(p[1].split(\":\")[1], 16)} -> {socket.inet_ntoa(struct.pack(\"<L\", int(p[2].split(\":\")[0], 16)))}:{int(p[2].split(\":\")[1], 16)}') for p in [l.split() for l in open('/proc/net/tcp').readlines()[1:]] if p[3] == '01']"
  ```
- Look for unrecognized UIDs (e.g., `70`) or suspicious paths disguised as legitimate services (e.g., `/tmp/postgresql`).
- **Sudo Workaround for Agents:** To kill processes owned by other users or `root`, `sudo` is required. If the user explicitly provides the `sudo` password for emergency response, automate execution without interactive prompts using `SUDO_ASKPASS`:
  ```bash
  cat << 'EOF' > /tmp/ap.sh
  #!/bin/bash
  echo "THE_PASSWORD"
  EOF
  chmod +x /tmp/ap.sh
  export SUDO_ASKPASS=/tmp/ap.sh
  
  sudo -A pkill -9 -u <suspicious_uid>
  sudo -A kill -9 <pid>
  
  rm -f /tmp/ap.sh
  ```

## 2. Docker Port Security (Critical Pitfall)
- **Pitfall:** Using `ports: - \"5432:5432\"` in `docker-compose.yml` binds the port to `0.0.0.0` across all interfaces, exposing it to the public internet. *Docker manipulates `iptables` directly, meaning this bypasses standard UFW deny rules.*
- **Solution:** Always bind internal databases (PostgreSQL, Redis, etc.) exclusively to localhost if they do not need public access, especially when sitting behind a reverse proxy like Traefik:
  ```yaml
  ports:
    - \"127.0.0.1:5432:5432\"
  ```

## 3. Firewall (UFW) Configuration
- Always enable UFW to establish a baseline deny-all policy for non-Docker traffic.
- Basic safe configuration:
  ```bash
  sudo -A ufw default deny incoming
  sudo -A ufw default allow outgoing
  sudo -A ufw allow ssh
  sudo -A ufw allow 80
  sudo -A ufw allow 443
  # Add other explicit ports here (e.g., 3000, 8000)
  echo \"y\" | sudo -A ufw enable
  ```
- *Note:* Remind the user to change their passwords immediately if a compromise has occurred and you were given the `sudo` password to perform the cleanup. Do NOT save the password to memory.