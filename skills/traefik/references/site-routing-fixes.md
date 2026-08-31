# Site routing fixes observed in production

## Issue: API paths returning Next.js 404 HTML instead of backend JSON
- Symptom: `curl -s https://<host>/api/...` returns Next.js 404 HTML, not JSON.
- Cause: The frontend host router matched `/api/...` before the API router, or new API paths were not excluded from the frontend router.
- Fix pattern for file-provider dynamic rules:
  1. Keep the frontend router broad but exclude API paths from it.
  2. Keep the backend router explicit and higher-priority for routed API/health/webhook paths.
  3. After dynamic rule changes, verify both:
     - `curl -I https://<host>/health` => backend
     - `curl -s https://<host>/api/<new-route>` => JSON, not HTML

## Example file-provider rule structure for Next.js + FastAPI
- Frontend app: `Host('<domain>')`
- Backend API: `Host('<domain>') && (PathPrefix('/webhooks') || (PathPrefix('/api') && !PathPrefix('/api/auth') && !PathPrefix('/api/<new-frontend-api-route>')) || PathPrefix('/health'))`
- Backend `priority` should be higher than the app router.

## Tip
- Traefik hits `Bad Gateway` during restarts when frontend/app containers are cold. Confirm container health first, then re-test from host.
