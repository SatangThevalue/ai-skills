---
name: tailscale-docker-zero-trust
description: Secure Docker container deployments by binding critical services explicitly to Tailscale VPN IPs (Zero-Trust) instead of 0.0.0.0 or 127.0.0.1.
version: 1.0.0
metadata:
  hermes:
    tags: [docker, security, tailscale, zero-trust, networking]
    category: devops
    requires_toolsets: [terminal]
---

# Tailscale Docker Zero-Trust

This skill outlines the architecture and procedure for securing internal Docker services (like databases, orchestrators, and secret vaults) by binding their exposed ports strictly to the host's Tailscale VPN IP address. 

## When to Use
- When deploying internal tools (Prefect, PostgreSQL, Infisical) on a VPS that should only be accessible to authorized devices, not the public internet.
- When `127.0.0.1` binding is too restrictive (preventing authorized remote team access) but `0.0.0.0` is too dangerous (exposing databases to automated attacks).

## Architecture Concept
By default, mapping ports in `docker-compose.yml` as `ports: ["5432:5432"]` binds the service to `0.0.0.0`, bypassing UFW firewalls and exposing it globally. 

Binding to `127.0.0.1:5432:5432` is secure but requires SSH tunneling to access from a remote machine.

Binding to the Tailscale IP (e.g., `100.115.66.121:5432:5432`) ensures the service is accessible to ANY device authenticated on the Tailscale network, while remaining completely invisible and unreachable from the public internet.

## Procedure

### 1. Identify the Tailscale IP
Find the Tailscale IPv4 address of the host machine:
```bash
ip addr show tailscale0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1
# Example output: 100.115.66.121
```

### 2. Update docker-compose.yml Port Bindings
Modify the `ports` mapping for internal services to explicitly use the Tailscale IP.

**Insecure (Publicly Exposed):**
```yaml
ports:
  - "5432:5432"
```

**Zero-Trust (Tailscale Only):**
```yaml
ports:
  - "100.115.66.121:5432:5432"
```

### 3. Update Inter-Service API URLs
If other services running on the host need to communicate with these bound services via their public/external URLs, ensure the environment variables point to the Tailscale IP rather than `localhost` or `127.0.0.1` to maintain consistent routing.

```yaml
environment:
  - PREFECT_API_URL=http://100.115.66.121:4200/api
```

### 4. Apply Changes
Restart the containers to apply the new bindings:
```bash
docker compose up -d
```

## Pitfalls
- **Dynamic Tailscale IPs:** If the machine leaves and re-joins the Tailnet under a different identity, the IP might change, breaking the hardcoded bindings in `docker-compose.yml`. Ensure the machine is authenticated with a stable, non-expiring key or that you update the compose files if the IP changes.
- **Wiping Databases on Compose Restart:** When tearing down and recreating containers to apply new port bindings, avoid running `docker compose down -v` unless you explicitly want to destroy the persistent volume data.
- **Docker Compose Version Attribute:** Modern versions of Docker Compose warn that the `version: "3.8"` attribute is obsolete. This warning is harmless but can clutter logs. Remove the `version` line from `docker-compose.yml` files when editing them.
- **Initial Password Seeding in 9Router/Apps:** When deploying apps like 9Router that seed an initial password to an SQLite database on first boot via environment variables (`INITIAL_PASSWORD`), if the container boots before the variable is set (or if the database was created empty), the password won't take effect. You must stop the container, delete the persistent SQLite database (wipe the volume), and start it again so the initialization script runs fresh with the correct environment variables.

## Verification
- Run `docker ps --format "table {{.Names}}\t{{.Ports}}"`. Verify the ports show the Tailscale IP (e.g., `100.115.66.121:5432->5432/tcp`).
- Attempt to connect to the port using the public IP of the VPS. It should fail or timeout.
- Attempt to connect to the port using the Tailscale IP from an authorized remote device. It should succeed.