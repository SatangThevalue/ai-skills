---
name: postgres-pgvector-traefik
description: Deploy PostgreSQL 18 with pgvector and Traefik TCP proxying.
version: 0.1.0
metadata:
  hermes:
    tags: [PostgreSQL, pgvector, Traefik, Docker, TCP-Proxy]
---

# PostgreSQL pgvector with Traefik TCP Proxy

Deploys PostgreSQL 18 with the `pgvector` extension via Docker Compose. It routes database traffic through Traefik using a TCP router, allowing you to proxy port 5432, log connections, and keep the database behind the reverse proxy network. 

## When to Use
- The user asks to deploy a vector database or PostgreSQL with `pgvector`.
- You need to route PostgreSQL or TCP traffic through an existing Traefik instance.
- You are setting up PostgreSQL 18+ and need the correct volume mount structure.

## Prerequisites
- A running Traefik instance connected to a Docker network (e.g., `traefik-public`).
- Access to the host to open firewall ports manually if `sudo` is required.
- Target credentials (username, password, database name).

## How to Run
Use `write_file` to create the PostgreSQL compose file, `patch` to update the Traefik entrypoints, and `terminal` to deploy and initialize the extension.

## Quick Reference
- Verify pgvector: `docker exec postgres psql -U <user> -d <db> -c '\dx vector'`
- Enable pgvector: `CREATE EXTENSION IF NOT EXISTS vector;`

## Procedure

1. **Update Traefik Static Config**
   Use `patch` to add the `postgresql` entrypoint to Traefik's `traefik.yml`:
   ```yaml
   entryPoints:
     postgresql:
       address: ":5432"
   ```

2. **Update Traefik Compose File**
   Use `patch` to expose port `5432:5432` in Traefik's `docker-compose.yml`, then apply with `terminal`:
   ```bash
   docker compose up -d
   ```

3. **Create PostgreSQL Compose File**
   Use `write_file` to create `docker-compose.yml` for PostgreSQL:
   ```yaml
   services:
     postgres:
       image: pgvector/pgvector:pg18
       container_name: postgres
       restart: unless-stopped
       environment:
         POSTGRES_USER: ${POSTGRES_USER:-myuser}
         POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-mypassword}
         POSTGRES_DB: ${POSTGRES_DB:-postgres}
         # Crucial for PG18: place data in a subdirectory
         PGDATA: /var/lib/postgresql/data/pgdata
       volumes:
         - pgdata:/var/lib/postgresql/data
       networks:
         - traefik-public
       labels:
         - "traefik.enable=true"
         - "traefik.tcp.routers.postgres.rule=HostSNI(`*`)"
         - "traefik.tcp.routers.postgres.entrypoints=postgresql"
         - "traefik.tcp.services.postgres.loadbalancer.server.port=5432"

   volumes:
     pgdata:

   networks:
     traefik-public:
       external: true
   ```

4. **Deploy and Initialize**
   Use `terminal` to start the database and enable the extension:
   ```bash
   docker compose up -d
   sleep 10
   docker exec postgres psql -U myuser -d postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```

5. **Open Firewall**
   Ask the user to run the firewall command manually if `sudo` requires a password:
   ```bash
   sudo ufw allow 5432/tcp
   ```

## Pitfalls
- **PostgreSQL 18 Volume Mount Error**: PostgreSQL 18+ strict mount constraints will fail if you mount directly to `/var/lib/postgresql/data`. You MUST set `PGDATA: /var/lib/postgresql/data/pgdata` (a subdirectory) to prevent `pg_upgrade --link` boundary issues.
- **Traefik HostSNI on TCP**: When proxying raw TCP without TLS termination in Traefik, you must use `HostSNI('*')`. Specific domain routing requires TLS.
- **Agent Sudo Blocks**: Do not attempt to pipe passwords into `sudo ufw allow`. Always instruct the user to execute it directly.

## Verification
Use the `terminal` tool to verify the extension was installed correctly:
```bash
docker exec postgres psql -U myuser -d postgres -c "\dx vector"
```
The output should list the `vector` extension and its version (e.g., `0.8.3`).