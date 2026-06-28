---
name: traefik-docker29-fix
description: Fix Traefik Docker API errors on Docker Engine 29.4 plus.
version: 0.1.0
metadata:
  hermes:
    tags: [Docker, Traefik, Bug-Fix, Networking, SSL]
---

# Traefik Docker Engine 29.4+ API Fix

Resolves "client version 1.24 is too old" and "Failed to list containers" errors when running Traefik with Docker Engine >= 29.4.1. This occurs because modern Docker Engine raised `MinAPIVersion` to 1.40, but Traefik's Go Docker SDK defaults to negotiating with `v1.24`. This skill uses a Python TCP relay to rewrite Docker API version requests from `< v1.40` to `v1.40` on the fly. It also catalogs Let's Encrypt ACME DNS challenge pitfalls discovered during Traefik provisioning.

## When to Use
- Traefik logs show `client version 1.24 is too old`.
- Traefik logs show `Failed to list containers for docker`.
- Setting `DOCKER_API_VERSION` environment variable in Traefik does not resolve the issue.
- Encountering "Permission Denied" or "server misbehaving" during Let's Encrypt DNS-01 challenges via Lego.

## Prerequisites
- A Docker Compose stack for Traefik.
- The `scripts/docker-relay.py` file available in the skill directory (accessible via `skill_view(name="traefik-docker29-fix", file_path="scripts/docker-relay.py")`).

## How to Run
Invoke through the `terminal` tool to modify the `docker-compose.yml` and Traefik static configuration.

## Procedure

1. Obtain the relay script using `skill_view` to read `scripts/docker-relay.py` from this skill, and write it to the Traefik deployment folder using the `write_file` tool (e.g., at `./config/docker-relay.py`).
2. Add the `docker-relay` service to `docker-compose.yml`:
```yaml
services:
  docker-relay:
    image: python:3.11-alpine
    container_name: traefik-docker-relay
    restart: unless-stopped
    privileged: true
    ports:
      - "127.0.0.1:2376:2376"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./config/docker-relay.py:/app/relay.py:ro
    command: python /app/relay.py
    networks:
      - socket-proxy
```
3. Attach the `traefik` service to the `socket-proxy` network and add `depends_on: [docker-relay]`.
4. Update Traefik's static configuration (`traefik.yml`) to point to the relay instead of the local unix socket:
```yaml
providers:
  docker:
    endpoint: "tcp://docker-relay:2376"
    exposedByDefault: false
    network: traefik-public
```
5. Restart the stack using `terminal`:
```bash
docker compose down && docker compose up -d
```

## Pitfalls

**ACME DNS Challenge Quirks (Name.com & Lego):**
- **"Permission Denied" error on DNS records:** This frequently happens if the API token environment variable contains a hidden trailing newline. Use `cat -A .env` to verify there are no `$` newline markers at the end of the token string. Write tokens using `echo -n` to prevent this.
- **"Server misbehaving" or `https//api.name.com` error:** Lego's Name.com provider automatically prepends `https://`. If you set `NAMECOM_SERVER=https://api.name.com`, Lego will dial `https://https//api.name.com`. Leave `NAMECOM_SERVER` unset for production, or specify just the hostname without the scheme if strictly required.
- **Duplicate Record error:** Sometimes Lego interprets a "Duplicate Record" API response as "Permission Denied". Manually delete lingering `_acme-challenge` TXT records via API or dashboard if validation repeatedly fails.

## Verification
Use the `terminal` tool to inspect the Traefik logs. The "Failed to retrieve information" error should be gone, and you should see a successful Docker provider initialization:
```bash
docker logs traefik | grep -i "provider connection established with docker"
```