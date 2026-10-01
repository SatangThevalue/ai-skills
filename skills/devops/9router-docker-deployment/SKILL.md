---
name: 9router-docker-deployment
description: "Deploy and troubleshoot 9Router via Docker and Tailscale with password/DB injection fixes."
version: 0.1.0
category: devops
---

# 9Router Docker Deployment & Troubleshooting

9Router is an AI Token Saver & Router. When deploying it via Docker, especially in isolated networks (Tailscale), specific configurations are required to ensure security and proper initialization.

## Quick Start (Docker Compose)
```yaml
version: "3.8"
services:
  9router:
    image: decolua/9router:latest
    container_name: 9router-app
    restart: always
    environment:
      - DATA_DIR=/app/data
      - INITIAL_PASSWORD=${INITIAL_PASSWORD:-your_password}
      - PORT=20128
      - HOSTNAME=0.0.0.0
    ports:
      # Bind to Tailscale IP for Zero-Trust
      - "100.x.y.z:20128:20128"
    volumes:
      - router_data:/app/data

volumes:
  router_data:
```

## ⚠️ Critical Pitfalls & Fixes

1. **INITIAL_PASSWORD Ignored / Lockout Issue (IP Binding):**
   If you bind 9Router to `0.0.0.0` (all interfaces) instead of a local/Tailscale IP, its security system detects remote exposure and blocks the default `123456` password, causing a lockout error: `Default password must be changed before remote access`.
   - **Fix:** You MUST explicitly set `INITIAL_PASSWORD=<your_secure_password>` in the `environment` block of `docker-compose.yml` to log in via remote IP.
   - **Alternative (Local/Tailscale only):** Remove `INITIAL_PASSWORD`, wipe the data directory, restart the container, and access via `127.0.0.1` or `100.x.x.x` to use `123456` and change it via UI.

2. **Permission Denied for WebUI / Non-Root Containers:**
   When running 9Router or similar apps (like Hermes WebUI) that drop privileges (e.g., running as UID 1024), do not mount volumes to `/root` or rely on Docker-managed volumes without proper permissions. This causes SQLite `Permission denied` errors.
   - **Fix:** Create a local folder (`mkdir data`), grant permissions (`chmod 777 data`), and mount it to `/app/data` in the container.

2. **Tailscale vs. Localhost Binding:**
   To prevent public exposure, bind the exposed ports strictly to the Tailscale IP (`100.x.y.z:20128:20128`). 
   **Exception:** If the OS host needs to connect via `localhost:20128` (or other containers need host-gateway access), you MUST bind to all interfaces (`20128:20128`). Strict Tailscale binding disables `localhost` loopback access.

3. **Background Process Required for Startup:**
   When running `docker compose up -d` in a Hermes agent session, **ALWAYS** use `terminal(background=true, notify_on_complete=true)`. Attempting to run it as a foreground process will cause the tool to fail or time out because it's interpreted as a long-lived server/watch process.