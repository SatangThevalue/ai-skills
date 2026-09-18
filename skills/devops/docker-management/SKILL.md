---
name: docker-management
description: Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization.
version: 1.0.0
author: sprmn24
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docker, containers, devops, infrastructure, compose, images, volumes, networks, debugging]
    category: devops
    requires_toolsets: [terminal]
---

# Docker Management

Manage Docker containers, images, volumes, networks, and Compose stacks using standard Docker CLI commands. No additional dependencies beyond Docker itself.

## When to Use

- Run, stop, restart, remove, or inspect containers
- Build, pull, push, tag, or clean up Docker images
- Work with Docker Compose (multi-service stacks)
- Manage volumes or networks
- Debug a crashing container or analyze logs
- Check Docker disk usage or free up space
- Review or optimize a Dockerfile

## Prerequisites

- Docker Engine installed and running
- User added to the `docker` group (or use `sudo`)
- Docker Compose v2 (included with modern Docker installations)

Quick check:

```bash
docker --version && docker compose version
```

- `references/postgres-miner-sudo-askpass.md` — Handling memory-resident PostgreSQL cryptominers when the user provides a password using the `SUDO_ASKPASS` technique.
- `references/memory-resident-malware-removal.md` — General workflow for identifying and removing memory-resident cryptominers.


| Task | Command |
|------|---------|
| Run container (background) | `docker run -d --name NAME IMAGE` |
| Stop + remove | `docker stop NAME && docker rm NAME` |
| View logs (follow) | `docker logs --tail 50 -f NAME` |
| Shell into container | `docker exec -it NAME /bin/sh` |
| List all containers | `docker ps -a` |
| Build image | `docker build -t TAG .` |
| Compose up | `docker compose up -d` |
| Compose down | `docker compose down` |
| Disk usage | `docker system df` |
| Cleanup dangling | `docker image prune && docker container prune` |

## Procedure

### 1. Identify the domain

Figure out which area the request falls into:

- **Container lifecycle** → run, stop, start, restart, rm, pause/unpause
- **Container interaction** → exec, cp, logs, inspect, stats
- **Image management** → build, pull, push, tag, rmi, save/load
- **Docker Compose** → up, down, ps, logs, exec, build, config
- **Volumes & networks** → create, inspect, rm, prune, connect
- **Troubleshooting** → log analysis, exit codes, resource issues

### 2. Container operations

**Run a new container:**

```bash
# Detached service with port mapping
docker run -d --name web -p 8080:80 nginx

# With environment variables
docker run -d -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=mydb --name db postgres:16

# With persistent data (named volume)
docker run -d -v pgdata:/var/lib/postgresql/data --name db postgres:16

# For development (bind mount source code)
docker run -d -v $(pwd)/src:/app/src -p 3000:3000 --name dev my-app

# Interactive debugging (auto-remove on exit)
docker run -it --rm ubuntu:22.04 /bin/bash

# With resource limits and restart policy
docker run -d --memory=512m --cpus=1.5 --restart=unless-stopped --name app my-app
```

Key flags: `-d` detached, `-it` interactive+tty, `--rm` auto-remove, `-p` port (host:container), `-e` env var, `-v` volume, `--name` name, `--restart` restart policy.

**Manage running containers:**

```bash
docker ps                        # running containers
docker ps -a                     # all (including stopped)
docker stop NAME                 # graceful stop
docker start NAME                # start stopped container
docker restart NAME              # stop + start
docker rm NAME                   # remove stopped container
docker rm -f NAME                # force remove running container
docker container prune           # remove ALL stopped containers
```

**Interact with containers:**

```bash
docker exec -it NAME /bin/sh          # shell access (use /bin/bash if available)
docker exec NAME env                   # view environment variables
docker exec -u root NAME apt update    # run as specific user
docker logs --tail 100 -f NAME         # follow last 100 lines
docker logs --since 2h NAME            # logs from last 2 hours
docker cp NAME:/path/file ./local      # copy file from container
docker cp ./file NAME:/path/           # copy file to container
docker inspect NAME                    # full container details (JSON)
docker stats --no-stream               # resource usage snapshot
docker top NAME                        # running processes
```

### 3. Image management

```bash
# Build
docker build -t my-app:latest .
docker build -t my-app:prod -f Dockerfile.prod .
docker build --no-cache -t my-app .              # clean rebuild
DOCKER_BUILDKIT=1 docker build -t my-app .       # faster with BuildKit

# Pull and push
docker pull node:20-alpine
docker login ghcr.io
docker tag my-app:latest registry/my-app:v1.0
docker push registry/my-app:v1.0

# Inspect
docker images                          # list local images
docker history IMAGE                   # see layers
docker inspect IMAGE                   # full details

# Cleanup
docker image prune                     # remove dangling (untagged) images
docker image prune -a                  # remove ALL unused images (careful!)
docker image prune -a --filter "until=168h"   # unused images older than 7 days
```

### 4. Docker Compose

```bash
# Start/stop
# PITFALL: Do not run `docker compose up -d` directly in the foreground terminal. It starts background daemon processes which the terminal tool rejects as "hanging". 
# ALWAYS use: terminal(command="cd /path && docker compose up -d", background=true, notify_on_complete=true)
# Note: Sometimes `docker-compose` is not found, always try `docker compose` as a fallback.
docker compose up -d                   # start all services detached
docker compose up -d --build           # rebuild images before starting
docker compose down                    # stop and remove containers
docker compose down -v                 # also remove volumes (DESTROYS DATA)
```

# Monitoring
docker compose ps                      # list services
docker compose logs -f api             # follow logs for specific service
docker compose logs --tail 50          # last 50 lines all services

# Interaction
docker compose exec api /bin/sh        # shell into running service
docker compose run --rm api npm test   # one-off command (new container)
docker compose restart api             # restart specific service

# Validation
docker compose config                  # validate and view resolved config
```

**Minimal compose.yml example:**

```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### 5. Volumes and networks

```bash
# Volumes
docker volume ls                       # list volumes
docker volume create mydata            # create named volume
docker volume inspect mydata           # details (mount point, etc.)
docker volume rm mydata                # remove (fails if in use)
docker volume prune                    # remove unused volumes

# Networks
docker network ls                      # list networks
docker network create mynet            # create bridge network
docker network inspect mynet           # details (connected containers)
docker network connect mynet NAME      # attach container to network
docker network disconnect mynet NAME   # detach container
docker network rm mynet                # remove network
docker network prune                   # remove unused networks
```

### 6. Common Build and Runtime Pitfalls

- **Build Resources (No space left on device):** Production builds (like Next.js `npm run build` inside a Dockerfile) consume significant RAM and disk space. In constrained environments, this often causes `no space left on device` errors during `docker compose build`. Clean up space aggressively (`docker system prune -af --volumes`) before retrying the build.
- **Port Conflicts:** When running containers via `docker-compose` or `docker run`, map a free port (e.g., `3001:3000` or `5433:5432`) if the host's target port is occupied by another local service, otherwise the container will fail to start with a `Bind for 0.0.0.0:XXXX failed: port is already allocated` error.
- **Dependency Resolution in Build:** When a `pip install` step in a Dockerfile fails due to `ResolutionImpossible`, loosen strict version pins (e.g., change `==` to `>=`) in the `requirements.txt` to allow the package manager to resolve shared underlying dependencies.

## Best Practices

### Security: Strict Port Binding
**Pitfall:** Defining ports as `- "5432:5432"` in `docker-compose.yml` binds to `0.0.0.0` by default, exposing the service (e.g., PostgreSQL, Redis) to the public internet. This leads directly to automated brute-force attacks and malware infections.
**Fix:** If a port must be accessible from the host but NOT the public internet, bind it strictly to `127.0.0.1`:
```yaml
ports:
  - "127.0.0.1:5432:5432"
```
If it only needs to be accessible to other containers (e.g., via Traefik or a Docker network), remove the `ports:` block entirely.

## Troubleshooting Common Errors

Always start with a diagnostic before cleaning:

```bash
# Check what's using space
docker system df                       # summary
docker system df -v                    # detailed breakdown

# Targeted cleanup (safe)
docker container prune                 # stopped containers
docker image prune                     # dangling images
docker volume prune                    # unused volumes
docker network prune                   # unused networks

# Aggressive cleanup (confirm with user first!)
docker system prune                    # containers + images + networks
docker system prune -a                 # also unused images
docker system prune -a --volumes       # EVERYTHING — named volumes too
```

**Warning:** Never run `docker system prune -a --volumes` without confirming with the user. This removes named volumes with potentially important data.

## Pitfalls
- **No Space Left on Device**: Docker builds (like `next build` or heavy `pip install` phases) can fail with `write ... no space left on device` on VPS instances with limited disk space. Run `docker system prune -af --volumes` to reclaim space before retrying the build.
- **Port Allocation Failures**: If starting a container fails with `Bind for 0.0.0.0:XXXX failed: port is already allocated`, edit the compose file to map to a free host port (e.g., change `"4200:4200"` to `"4202:4200"`).
- **Host Volume Permissions**: When mounting host directories (e.g., for Next.js), the container user might not have write access, causing `EACCES` during build/run. Fix it by running an alpine container temporarily to adjust permissions: `docker run --rm -v $(pwd):/app alpine chown -R 1000:1000 /app/<dir>`.
- **Container-to-Host `localhost` Routing**: `localhost`/`127.0.0.1` inside a container points to the container itself, not the host. If a host process (proxy, local API, dev server) must be reached from a container, `curl http://localhost:PORT` will fail with `Connection refused`. Fix: use the Docker bridge IP of the host interface on the same network, typically `ip route show table local` or `ip addr show` to find the bridge IP (e.g., `10.0.2.1`), then expose that host port to the container via compose `environment:` rather than hardcoding IPs in application code. Prefer an env var like `HOST_GATEWAY`/`AI_PROXY_URL` so the same image works both locally and in Docker.
- **Malware in RAM (Postgres/Redis exploits):** If the VPS runs out of RAM and you spot a suspicious process (like `/tmp/postgresql` running under an unknown user like `70`) consuming massive memory, it is likely a cryptominer exploiting weak container credentials or open ports (e.g., exposed PostgreSQL without a password). These malware variants often delete their own binaries from `/tmp` and run entirely in memory. To fix: the agent will NOT be able to kill it via `sudo` due to password blocks. Advise the user to SSH in and manually run `sudo kill -9 <PID>`, followed by `sudo reboot` to clear the RAM. Alternatively, if the user explicitly provides their root password, you can execute the kill command via `export SUDO_ASKPASS=/tmp/ap.sh` using a temporary executable script that echoes the password. After reboot or kill, review Docker container port bindings (e.g., bind DB ports to `127.0.0.1:5432:5432` rather than `0.0.0.0` in `docker-compose.yml`), strengthen passwords, and ensure the host firewall (UFW) is active and blocking external database access.
| Problem | Cause | Fix |
|---------|-------|-----|
| Container-to-host service `Connection refused` | App inside Docker uses `localhost:PORT` but service runs on host | Use env var + Docker bridge IP in compose; see `cli-proxy-api-troubleshooting` skill references for pattern |
| Container exits immediately | Main process finished or crashed | Check `docker logs NAME`, try `docker run -it --entrypoint /bin/sh IMAGE` |
| "docker-compose: command not found" | Legacy docker-compose standalone binary is missing | Use the modern Compose plugin via `docker compose` instead |
| "port is already allocated" | Another process using that port | `docker ps` or `lsof -i :PORT` to find it |
| "no space left on device" | Docker disk full | `docker system df` then targeted prune |
| Can't connect to container | App binds to 127.0.0.1 inside container | App must bind to `0.0.0.0`, check `-p` mapping |
| Permission denied on volume | UID/GID mismatch host vs container | Use `--user $(id -u):$(id -g)` or fix permissions |
| Compose services can't reach each other | Wrong network or service name | Services use service name as hostname, check `docker compose config` |
| Build cache not working | Layer order wrong in Dockerfile | Put rarely-changing layers first (deps before source code) |
| Image too large | No multi-stage build, no .dockerignore | Use multi-stage builds, add `.dockerignore` |
| Client version is too old | Modern Docker Engine (29.4+) raised MinAPIVersion to 1.40 | SDKs (like Traefik's) negotiating with <1.40 will fail. Workaround: deploy a TCP relay (e.g., `traefik-docker29-fix`) to rewrite the API version in flight. |

## Verification

After any Docker operation, verify the result:

- **Container started?** → `docker ps` (check status is "Up")
- **Logs clean?** → `docker logs --tail 20 NAME` (no errors)
- **Port accessible?** → `curl -s http://localhost:PORT` or `docker port NAME`
- **Volume mounted?** → `docker inspect -f '{{ .Mounts }}' NAME`
- **Network connected?** → `docker network inspect NAME`
- **Disk freed?** → `docker system df` (compare before/after)

## Security Pitfalls
- **Exposed Database Ports:** Never map database ports (e.g., `5432:5432`) to `0.0.0.0` on a public VPS. This exposes the database to the internet, inviting brute-force attacks and malware injections (e.g., cryptominers installed via OS command execution vulnerabilities). **Always bind to localhost** (e.g., `127.0.0.1:5432:5432`) unless explicit public access is required and secured by a firewall.
- **Unrestricted Firewall:** Relying solely on Docker's port mapping without a host firewall (like UFW) is dangerous. Enable UFW, set default incoming to `deny`, and explicitly `allow` only required ports (22, 80, 443).

## Dockerfile Optimization Tips

When reviewing or creating a Dockerfile, suggest these improvements:

1. **Multi-stage builds** — separate build environment from runtime to reduce final image size
2. **Layer ordering** — put dependencies before source code so changes don't invalidate cached layers
3. **Combine RUN commands** — fewer layers, smaller image
4. **Use .dockerignore** — exclude `node_modules`, `.git`, `__pycache__`, etc.
5. **Pin base image versions** — `node:20-alpine` not `node:latest`
6. **Run as non-root** — add `USER` instruction for security
7. **Use slim/alpine bases** — `python:3.12-slim` not `python:3.12`
8. **Port Security (Zero-Trust)** — Never expose database ports (e.g., PostgreSQL `5432`, Redis `6379`) or internal services to `0.0.0.0` unless explicitly required and secured by external firewalls. Always bind to localhost (`127.0.0.1:<port>:<port>`) for services placed behind a reverse proxy (like Traefik) to prevent brute-force attacks and malware/cryptominer infections.
