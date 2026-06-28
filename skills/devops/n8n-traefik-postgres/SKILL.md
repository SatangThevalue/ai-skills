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

## Procedure

1. **Provision the Database**
   Invoke through the `terminal` tool to execute `psql` inside the existing PostgreSQL container:
   ```bash
   docker exec postgres psql -U <admin_user> -d postgres -c "CREATE USER n8n_user WITH PASSWORD 'n8n_password';"
   docker exec postgres psql -U <admin_user> -d postgres -c "CREATE DATABASE n8n OWNER n8n_user;"
   ```

2. **Create the n8n Compose File**
   Use `write_file` to author `docker-compose.yml`. Replace placeholders with actual values:
   ```yaml
   services:
     n8n:
       image: docker.n8n.io/n8nio/n8n
       container_name: n8n
       restart: unless-stopped
       ports:
         - "5678:5678"
       environment:
         - DB_TYPE=postgresdb
         - DB_POSTGRESDB_DATABASE=n8n
         - DB_POSTGRESDB_HOST=postgres
         - DB_POSTGRESDB_PORT=5432
         - DB_POSTGRESDB_USER=n8n_user
         - DB_POSTGRESDB_PASSWORD=n8n_password
         - N8N_HOST=n8n.example.com
         - N8N_PORT=5678
         - N8N_PROTOCOL=https
         - NODE_ENV=production
         - WEBHOOK_URL=https://n8n.example.com/
         - GENERIC_TIMEZONE=UTC
       volumes:
         - n8n_data:/home/node/.n8n
       networks:
         - traefik-public
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.n8n.rule=Host(`n8n.example.com`)"
         - "traefik.http.routers.n8n.entrypoints=websecure"
         - "traefik.http.routers.n8n.tls=true"
         - "traefik.http.routers.n8n.tls.certresolver=myresolver"
         - "traefik.http.services.n8n.loadbalancer.server.port=5678"
         # Mandatory headers for Webhooks
         - "traefik.http.middlewares.n8n-headers.headers.customrequestheaders.X-Forwarded-Proto=https"
         - "traefik.http.routers.n8n.middlewares=n8n-headers"

   volumes:
     n8n_data:

   networks:
     traefik-public:
       external: true
   ```

3. **Deploy**
   Invoke through the `terminal` tool to start the service in the background:
   ```bash
   docker compose up -d
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