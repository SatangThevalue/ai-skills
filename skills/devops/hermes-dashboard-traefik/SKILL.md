---
name: hermes-dashboard-traefik
description: Expose Hermes Dashboard via Traefik with SSL and systemd.
version: 0.1.0
author: Tonthong
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [Hermes, DevOps, Traefik, Security, Systemd]
---

# Expose Hermes Dashboard via Traefik with SSL and systemd

This skill provides a step-by-step workflow to configure, run, and expose the Hermes Web Dashboard securely behind a Traefik reverse proxy using SSL certificates and a systemd user service.

This guide does not cover configuring third-party OAuth providers, which should be set up via Nous Portal or custom configurations if needed.

## When to Use

- Exposing the local Hermes Web Dashboard to a remote domain (e.g., `https://dashboard.example.com`).
- Setting up the dashboard to run persistently in the background on system boot using systemd.
- Restricting dashboard access using secure password hashes instead of plaintext keys.

## Prerequisites

- Traefik reverse proxy running in a Docker container on the host.
- Python 3 with the `web` extras installed in the active Hermes virtual environment (e.g. `uv pip install -e ".[web,pty]"`).
- Standard Dynamic File Provider path mapped in the Traefik static configuration (e.g. `providers.file.directory` point to `/etc/traefik/dynamic`).

## How to Run

1. Generate and configure the security keys for Basic Auth.
2. Create and enable the Systemd service using the `terminal` tool.
3. Apply the dynamic routing configuration file to Traefik using the `write_file` tool.

## Quick Reference

- **Config Path:** `~/.hermes/config.yaml`
- **Dashboard keys:**
  - `dashboard.basic_auth.username`
  - `dashboard.basic_auth.password_hash`
  - `dashboard.basic_auth.secret`
- **Systemd user service path:** `~/.config/systemd/user/hermes-dashboard.service`

## Procedure

### Step 1: Generate Scrypt Password Hash
Do not write plaintext passwords. Generate a secure scrypt hash using the Python helper from the Hermes directory:
```bash
python3 -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('YOUR_SECURE_PASSWORD'))"
```

### Step 2: Configure basic auth in config.yaml
Write the configuration options to the config file (replace the variables with your generated values):
```bash
hermes config set dashboard.basic_auth.username "YOUR_USERNAME"
hermes config set dashboard.basic_auth.password_hash "scrypt$16384$8$1$..."
# Generate a random 32-byte secret hex for JWT signing
hermes config set dashboard.basic_auth.secret "$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
```

### Step 3: Create Systemd User Service
Write a user service configuration to run the dashboard headless in the background. Use the `write_file` tool to save this to `~/.config/systemd/user/hermes-dashboard.service`:
```ini
[Unit]
Description=Hermes Agent Web Dashboard
After=network.target

[Service]
Type=simple
ExecStart=/home/YOUR_USER/.local/bin/hermes dashboard --host 0.0.0.0 --port 9119 --no-open
Restart=always
RestartSec=5
WorkingDirectory=/home/YOUR_USER

[Install]
WantedBy=default.target
```
*Note: Bind host to `0.0.0.0` to allow the Docker bridge network to communicate with it, or `127.0.0.1` if Traefik is running on host network.*

### Step 4: Start and Enable the Dashboard Service
Run the following commands using the `terminal` tool to start the service:
```bash
systemctl --user daemon-reload
systemctl --user enable hermes-dashboard --now
```

### Step 5: Configure Traefik Dynamic File Route
Write the dynamic configuration using the `write_file` tool to your Traefik dynamic configuration directory (e.g. `/home/user/docker/traefik/config/dynamic/hermes.yml`):
```yaml
http:
  routers:
    hermes-dashboard:
      rule: Host(`dashboard.example.com`)
      entryPoints:
        - websecure
      service: hermes-dashboard-srv
      tls:
        certResolver: namecom # replace with your certResolver name

  services:
    hermes-dashboard-srv:
      loadBalancer:
        servers:
          # Use host gateway IP to route out of docker container to VPS localhost port
          - url: http://10.0.2.1:9119 
```
*Note: Retrieve host IP address inside the docker network bridge by checking `docker network inspect <network_name>`.*

## Pitfalls

- **Inside-Gateway Systemd Restarts:** Do not run `systemctl --user restart hermes-dashboard` inside an agent session spawned by the gateway. The gateway will kill the process tree before it can complete, resulting in a blocked command. Run `kill <PID>` instead to let systemd restart it automatically, or execute restarts from outside.
- **Docker host.docker.internal resolution:** On Linux, `host.docker.internal` might resolve to the default docker bridge interface (`10.0.0.1`) rather than the custom user bridge (e.g. `10.0.2.1`). Hardcode the bridge's Gateway IP inside Traefik configuration if routing fails with a 502 Bad Gateway.

## Verification

Test the response using the `terminal` tool to verify dynamic SSL routing and basic auth redirect are operational:
```bash
curl -I -k https://dashboard.example.com
```
You should get a `302 Found` response directing you to `/login?next=%2F`.
