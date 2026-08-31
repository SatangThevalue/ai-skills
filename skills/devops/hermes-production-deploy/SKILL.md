---
name: hermes-production-deploy
description: Procedural best practices for deploying Node.js (Next.js) and Python (FastAPI) SaaS applications on Hermes-managed VPS with Docker/Traefik.
---

# Production Deployment Checklist

## 1. Environment Readiness
- **Disk Management**: Always check `df -h` before `docker build`. If >80%, run `docker system prune -f` proactively.
- **Port Management**: Ensure `docker-compose.yml` does not bind host ports used by Traefik (80, 443). Use internal network for inter-container communication.
- **Credential Handling**: Never hardcode secrets in `main.py`, `admin_routes.py`, `auth.ts`, or any source file. Inject via `.env`, `docker-compose` env blocks, or CI/CD secrets. For feature flags/admin keys, reference `process.env.NEXT_PUBLIC_*` in Next.js and `os.getenv` in Python, with a fallback only for local development.
- **Verified URL Protocol**: When calling external/internal APIs from scripts, always confirm the scheme/port with a real `curl` before returning the URL to the user. Do not trust assumption that `http://` lives at the same address as `https://`.

## 2. Docker & Build Reliability
- **Next.js Build**: Always set `ENV CI=true` and `pnpm config set confirmModulesPurge false` in Dockerfile for automated CI/CD environments.
- **Production Build**: Use `next build` inside the builder stage.
- **Persistence**: Ensure volumes for database (Postgres) are defined to prevent data loss on container recreation.

## 3. Verification Protocol (CRITICAL)
- **Status Check**: After every `docker compose up`, verify with `docker ps`.
- **Health Verification**: Use `curl -I <URL>` to verify HTTP 200/404 before confirming success to the user.
- **Rebuild After Code-Only Changes**: Edits to FastAPI source (`admin_routes.py`, `ai_parser.py`) or `.env` references do not propagate to running containers automatically. Run `docker compose up -d --build <service>` before retesting.
- **Container->Host Service Access**: A container cannot reach host-bound services through `localhost`. Inspect the Compose network gateway (`docker network inspect <project>_default | grep Gateway`), use that IP/port externally, and verify with `docker exec <container> curl -s http://<gateway_ip>:<port>`.
- **GET vs HEAD**: Some FastAPI routers allow only GET. If `HEAD /health` returns 405, use `curl -s http://host:port/health` for a JSON probe.
- **Log Monitoring**: Use `docker compose logs -f <service>` immediately after deployment to catch startup errors.

## 4. Troubleshooting
- **Address already in use**: Always `pkill` remaining Uvicorn/Next processes on host before starting Docker containers.
- **DB Connection**: Ensure container hostnames (e.g., `satangthebank-db`) match the `DATABASE_URL` env variable.
