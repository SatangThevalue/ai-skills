# Next.js + Traefik routing sanity checks

Use this when a Next.js app is co-hosted with a backend API behind Traefik file-provider rules.

1. After adding any new frontend API route like `/api/<route>`, update file-provider backend rules to exclude it from the frontend app router.
2. Confirm Next.js did not publish a 404 for that route: `curl -s https://<host>/api/<route>` should not return HTML starting with `<!DOCTYPE html><html ...404...`.
3. If `/health` returns `405 Method Not Allowed`, note that the rule still matched the backend API router; that is often fine. Verify with `curl -s https://<host>/health` expecting `{"status":"ok"}`.

# Docker image rebuild checklist

In multi-service Docker Compose projects, source changes inside service build contexts are ignored on `restart`.

Required sequence after source edits:
- backend: `docker compose -f docker-compose.prod.yml build --no-cache <service>` then `docker compose up -d <service>` or `restart <service>`
- frontend: same build then restart
- verify container-internal copied source matches host: `docker compose exec <service> cat <copied-path>`
