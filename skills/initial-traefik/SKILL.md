---
name: initial-traefik
description: Initialize and configure Traefik reverse proxy with Docker. Install Traefik, configure Docker Compose, set up service routing via path prefix or host-based routing, enable features like dashboard metrics logging tracing, configure Dashboard access via nip.io or path prefix
---

# Initial Traefik

Initialize and configure Traefik v3 reverse proxy with Docker Compose for service routing and load balancing.

## Quick Start

### 1. Create Configuration

```bash
mkdir -p ~/.docker/compose
cd ~/.docker/compose
```

### 2. Create docker-compose.yml

Use `assets/docker-compose.yml` as template. Key configuration:

```yaml
services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik-dynamic.yml:/etc/traefik/dynamic.yml:ro
    command:
      - --api=true
      - --api.dashboard=true
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --providers.file.directory=/etc/traefik
      - --providers.file.watch=true
      - --entrypoints.web.address=:80
      - --accesslog=true
      - --metrics.prometheus=true
```

### 3. Create Dynamic Configuration

Use `assets/traefik-dynamic.yml` as template for service routing.

### 4. Start Traefik

```bash
docker compose up -d
```

### 5. Connect Services to Network

```bash
for container in <service-names>; do
  docker network connect compose_default $container
done
```

## Routing Options

### Option A: Path Prefix Routing (IP + Path)

Access services via `http://<IP>/<service>`:

```yaml
http:
  routers:
    n8n:
      rule: "PathPrefix(`/n8n`)"
      service: n8n
      entryPoints:
        - web
      middlewares:
        - n8n-stripprefix
  
  middlewares:
    n8n-stripprefix:
      stripPrefix:
        prefixes:
          - /n8n
  
  services:
    n8n:
      loadBalancer:
        servers:
          - url: "http://n8n:5678"
```

Access: `http://192.168.9.192/n8n`

### Option B: Host-Based Routing (.nip.io)

Access services via `http://<service>.<IP>.nip.io`:

```yaml
http:
  routers:
    n8n:
      rule: "Host(`n8n.192.168.9.192.nip.io`)"
      service: n8n
      entryPoints:
        - web
  
  services:
    n8n:
      loadBalancer:
        servers:
          - url: "http://n8n:5678"
```

Access: `http://n8n.192.168.9.192.nip.io`

### Option C: Docker Labels

Configure routing directly in docker-compose.yml labels:

```yaml
services:
  traefik:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.192.168.9.192.nip.io`)"
      - "traefik.http.routers.dashboard.service=api@internal"
      - "traefik.http.routers.dashboard.entrypoints=web"
```

### Option D: Apex-to-WWW Redirect (Docker Labels)

Use this common pattern to redirect traffic from the apex domain to `www` (e.g., `example.com` → `www.example.com`):

```yaml
services:
  web:
    labels:
      - "traefik.enable=true"
      # Route for www
      - "traefik.http.routers.web-www.rule=Host(`www.example.com`)"
      - "traefik.http.routers.web-www.entrypoints=websecure"
      - "traefik.http.routers.web-www.tls=true"
      - "traefik.http.routers.web-www.tls.certresolver=myresolver"
      - "traefik.http.services.web-www.loadbalancer.server.port=3000"
      
      # Route for apex (redirects to www)
      - "traefik.http.routers.web-apex.rule=Host(`example.com`)"
      - "traefik.http.routers.web-apex.entrypoints=websecure"
      - "traefik.http.routers.web-apex.tls=true"
      - "traefik.http.routers.web-apex.tls.certresolver=myresolver"
      - "traefik.http.routers.web-apex.middlewares=redirect-to-www"
      
      # Middleware configuration (note the double $$ for Docker Compose escape)
      - "traefik.http.middlewares.redirect-to-www.redirectregex.regex=^https://example.com/(.*)"
      - "traefik.http.middlewares.redirect-to-www.redirectregex.replacement=https://www.example.com/$${1}"
```

## Enable Features

See `references/features.md` for complete feature list and configuration.

## Common Tasks

### Add New Service

1. Connect container to network:
   ```bash
   docker network connect compose_default <container-name>
   ```

2. Add router to `traefik-dynamic.yml`:
   ```yaml
   routers:
     myservice:
       rule: "PathPrefix(`/myservice`)"
       service: myservice
       entryPoints:
         - web
       middlewares:
         - myservice-stripprefix
   
   services:
     myservice:
       loadBalancer:
         servers:
           - url: "http://<container-name>:<port>"
   ```

Traefik auto-reloads configuration.

### Check Status

```bash
docker logs traefik | grep -E "router|error"
docker exec traefik wget -q -O - http://localhost:8080/api/http/routers
```

### Restart Traefik

```bash
docker restart traefik
```

## Workflows and Architectures

### Monorepo / Micro-Frontend Routing
When separating frontend and backend traffic in a single domain space:
1. Define a `websecure` entrypoint for both routers.
2. Route the backend via `PathPrefix` (e.g., `/api`, `/webhooks`) with higher priority (e.g., `priority: 200`).
3. Route the frontend to the apex domain (e.g., `Host('example.com')`) with a lower priority (e.g., `priority: 100`) as a catch-all for UI routes.
4. If frontend and backend are running locally without Docker networks, map them via `host.docker.internal:<port>`.

Example (`dynamic.yml`):
```yaml
http:
  routers:
    api-router:
      rule: Host(`app.example.com`) && (PathPrefix(`/webhooks`) || PathPrefix(`/api`))
      entryPoints: ["websecure"]
      service: api-srv
      priority: 200
      tls:
        certResolver: namecom

    web-router:
      rule: Host(`app.example.com`)
      entryPoints: ["websecure"]
      service: web-srv
      priority: 100
      tls:
        certResolver: namecom

  services:
    api-srv:
      loadBalancer:
        servers:
          - url: http://host.docker.internal:8000
    web-srv:
      loadBalancer:
        servers:
          - url: http://host.docker.internal:3000
```

## References

- **Features**: See `references/features.md` for all available features
- **Examples**: See `references/examples.md` for common configurations
- **Templates**: See `assets/` for configuration templates

## Troubleshooting

- **Port Collision**: If `5432` is already bound by an existing PostgreSQL container, Traefik or a new compose stack will fail to bind `0.0.0.0:5432`. Either stop the conflicting service, or map the new container to an alternate port on the host (e.g., `5433:5432`).
- **Docker Compose + pnpm install**: When running `pnpm install` in a Dockerfile without a TTY, pnpm may block and wait for confirmation to purge the modules directory (`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`). Set `ENV CI=true` and run `RUN pnpm config set confirmModulesPurge false` before `pnpm install`.
- **404 errors**: Check container is connected to `compose_default` network
- **Configuration not loading**: Check `traefik-dynamic.yml` YAML syntax
- **Service not accessible**: Verify container name and port in service configuration
- **Dashboard not working**: Ensure `--api.dashboard=true` is in command
- **Docker 29.4+ "client version 1.24 is too old"**: Docker Engine 29.4+ raised `MinAPIVersion` to 1.40. Traefik defaults to negotiating with `v1.24`. Use the `traefik-docker29-fix` skill to deploy a TCP proxy to rewrite the requests.
- **Name.com DNS Challenge "Permission Denied"**: Usually caused by a trailing newline in the API token (e.g. from `.env` files). Ensure tokens are exported strictly without newlines (`echo -n "..." > .env`).
- **Name.com DNS Challenge "server misbehaving" (dial tcp: lookup https on 127.0.0.11:53)**: Lego prefixes `https://` to `NAMECOM_SERVER`. If `NAMECOM_SERVER=https://api.name.com`, Lego dials `https://https//api.name.com`. Leave `NAMECOM_SERVER` out of configuration for production defaults.
- **Host vs Next.js Container routing clash:** Be careful when writing dynamic router rules for multiple services sharing the same domain. Ensure you map API traffic (`PathPrefix('/api')`) with a higher `priority` (e.g. 200) than the catch-all frontend Next.js app routing (priority 100), to prevent Next.js from intercepting backend requests.
- **Docker 29.4+ API version error**: See `traefik` skill `scripts/docker_api_relay.py` for a workaround for Traefik's `client version 1.24 is too old` error when discovering containers.
