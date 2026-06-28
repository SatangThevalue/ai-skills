---
name: n8n-traefik-postgres
description: Deploy n8n with PostgreSQL via Traefik with required headers.
version: 0.1.0
metadata:
  hermes:
    tags: [n8n, PostgreSQL, Traefik, Docker, Headers]
---

# n8n with PostgreSQL on Traefik

Deploys an `n8n` automation server backed by a custom PostgreSQL database (instead of the default SQLite). Crucially, it sets up Traefik proxy headers (`X-Forwarded-Proto`) which are strictly required for n8n Webhooks and the UI to function securely over HTTPS.

## When to Use
- The user requests an `n8n` deployment.
- The user wants `n8n` to connect to a PostgreSQL database.
- The user wants `n8n` exposed over HTTPS using Traefik.

## Prerequisites
- A running PostgreSQL database (e.g., from `postgres-pgvector-traefik`).
- A running Traefik instance connected to a Docker network (e.g., `traefik-public`).
- Domain name mapped to the server IP.

## How to Run
Invoke through the `terminal` tool to provision the PostgreSQL user/database, use `write_file` to author the compose configuration, and use `terminal` to deploy the stack in the background.

## Quick Reference
- Create Postgres User: `CREATE USER n8n_user WITH PASSWORD 'secret';`
- Create Postgres DB: `CREATE DATABASE n8n OWNER n8n_user;`
- Required Traefik Header Label: `"traefik.http.middlewares.n8n-headers.headers.customrequestheaders.X-Forwarded-Proto=https"`
- Local MCP Tools for n8n:
  - `health` — Check API reachability & Docker status
  - `list_workflows` — List workflows (active filter)
  - `get_workflow` — Inspect a workflow (redacted secrets)
  - `list_executions` — List execution history
  - `activate_workflow` / `deactivate_workflow` — Mutate workflow states

## Procedure

1. **Deploy n8n and PostgreSQL**
   Refer to the docker-compose template to spin up n8n and PostgreSQL behind Traefik (ensure `X-Forwarded-Proto` header is set to `https`).

2. **Configure n8n MCP Server for Hermes**
   If you want Hermes to control or inspect n8n workflows directly, install and configure the stdio MCP bridge:
   ```bash
   # 1. Install the MCP bridge
   hermes mcp install n8n
   
   # 2. Store n8n credentials securely
   mkdir -p ~/.config/n8n-mcp
   cat > ~/.config/n8n-mcp/env <<'EOF'
   N8N_BASE_URL=http://127.0.0.1:5678
   N8N_API_KEY=your_n8n_token
   N8N_CONTAINER_NAME=n8n
   EOF
   chmod 600 ~/.config/n8n-mcp/env
   
   # 3. Configure the server parameters
   hermes config set mcp_servers.n8n.command "/home/thaieasyvps/.hermes/mcp-installs/n8n/.venv/bin/python"
   # Make sure args is saved as a JSON array list, NOT a raw string
   python3 -c "
   import yaml
   path = '/home/thaieasyvps/.hermes/config.yaml'
   with open(path) as f:
       data = yaml.safe_load(f)
   data['mcp_servers']['n8n']['args'] = ['/home/thaieasyvps/.hermes/mcp-installs/n8n/server.py']
   data['mcp_servers']['n8n']['env'] = {'N8N_MCP_ENV': '/home/thaieasyvps/.config/n8n-mcp/env'}
   with open(path, 'w') as f:
       yaml.safe_dump(data, f)
   "
   ```

3. **Verify the MCP bridge connection**
   ```bash
   hermes mcp test n8n
   ```

## Pitfalls
- **Missing `X-Forwarded-Proto`:** Without the custom request header middleware in Traefik, n8n will struggle with WebSocket connections, Webhook URLs will default to `http://` instead of `https://`, and the UI may warn about connection issues.
- **Python Missing Warning:** n8n logs may complain about Python 3 missing for the Task Runner. This is normal and expected when using internal mode.
- **Database Scope Migration:** During the first startup, n8n takes time to run database schema migrations. Wait for `Editor is now accessible via:` in the logs before assuming it's ready.

## Verification
Use the `terminal` tool to monitor the migration and startup process:
```bash
docker logs n8n --tail 20
```
Expect to see `Editor is now accessible via: https://n8n.example.com`.