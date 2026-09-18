# Docker Infrastructure Baseline

A proven safe starting point for a Zero-Touch Operations VPS setup using Docker Compose.

1. **Gateway** (Traefik) handling reverse proxy and SSL.
2. **Vault** (PostgreSQL) tightly bound to localhost.
3. **Orchestrator** (Prefect) bound to localhost.

## traefik/docker-compose.yml
```yaml
version: "3.8"
services:
  traefik:
    image: traefik:v3.3
    container_name: traefik-proxy
    restart: always
    command:
      - "--api.insecure=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - core_network
networks:
  core_network:
    external: true
```

## postgres/docker-compose.yml
```yaml
version: "3.8"
services:
  postgres:
    image: postgres:16-alpine
    container_name: vault-db
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: main_db
    ports:
      - "127.0.0.1:5432:5432" # CRITICAL: Block public access
    volumes:
      - vault_pgdata:/var/lib/postgresql/data
    networks:
      - core_network
volumes:
  vault_pgdata:
networks:
  core_network:
    external: true
```

## prefect/docker-compose.yml
```yaml
version: "3.8"
services:
  prefect:
    image: prefecthq/prefect:2-python3.11
    container_name: prefect-server
    restart: always
    command: ["prefect", "server", "start", "--host", "0.0.0.0"]
    environment:
      - PREFECT_API_URL=http://127.0.0.1:4200/api
      - PREFECT_SERVER_API_HOST=0.0.0.0
    ports:
      - "127.0.0.1:4200:4200" # CRITICAL: Block public access
    volumes:
      - prefect_data:/root/.prefect
    networks:
      - core_network
volumes:
  prefect_data:
networks:
  core_network:
    external: true
```