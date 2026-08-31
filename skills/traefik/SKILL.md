---
name: Traefik
description: Avoid common Traefik mistakes — router priority, TLS configuration, Docker labels syntax, and middleware ordering.
metadata: {"clawdbot":{"emoji":"🔀","os":["linux","darwin","win32"]}}
---

## Router Basics
- Router must have `rule` AND `service` — missing either = not working
- Rule priority: longer rules win by default — explicit `priority` to override
- `Host()` is case-insensitive — `Host(\`example.com\`)` matches Example.com
- Multiple hosts: `Host(\`a.com\`) || Host(\`b.com\`)` — OR logic

## Docker Labels Syntax
- Labels on container, not compose service level — `deploy.labels` for Swarm
- Backticks for rules in Docker Compose — `Host(\`example.com\`)` with escaping
- Enable per-container: `traefik.enable=true` — if `exposedByDefault=false`
- Service name auto-generated from container — or set explicitly with `traefik.http.services.myservice.loadbalancer.server.port=80`

## TLS and Certificates
- EntryPoint `websecure` needs TLS config — otherwise plain HTTP on 443
- Let's Encrypt: `certificatesResolvers.myresolver.acme.email` required — registration fails without
- HTTP challenge needs port 80 open — DNS challenge for wildcard or closed 80
- `tls=true` on router activates TLS — `tls.certresolver=myresolver` for auto-cert
- Staging ACME for testing — `caServer` to staging URL, avoids rate limits
- **Name.com provider quirk**: If `NAMECOM_SERVER` is set to `https://api.name.com`, Lego will dial `https://https//api.name.com` and fail with "server misbehaving". Set it to `api.name.com` or leave it blank (defaults to production).
- Staging server: use `caServer: https://acme-staging-v02.api.letsencrypt.org/directory` until working to avoid rate limits

## EntryPoints
- Define in static config — `--entrypoints.web.address=:80`
- Redirect HTTP to HTTPS at entrypoint level — cleaner than per-router middleware
- Router binds to entrypoint with `entryPoints=web,websecure` — comma-separated list

## Middlewares
- Chain order matters — first middleware wraps all following
- Middleware defined once, used by many routers — `middlewares=auth,compress`
- Common: `stripPrefix`, `redirectScheme`, `basicAuth`, `rateLimit`
- BasicAuth: use `htpasswd` format — escape `$` in Docker Compose with `$$`

## Service Configuration
- `loadbalancer.server.port` when container exposes multiple — Traefik can't guess
- Health check: `healthcheck.path=/health` — removes unhealthy from rotation
- Sticky sessions: `loadbalancer.sticky.cookie.name=srv_id` — for stateful apps

## Common Mistakes
- **Docker Compose Networking Errors**: When getting `network web declared as external, but could not be found`, verify the actual name of the Traefik network on the host (`docker network ls`). Usually, it is `traefik-public` or `proxy`, not `web`. Match your `networks` block and `labels` to the existing Traefik network.
- **Docker Compose Project Separation (502 Bad Gateway)**: If Traefik is set up via a file provider (or docker label discovery) to route queries to a domain using internal container names (e.g. `http://satangthebank-web:3000`), the application's Compose stack *must* be connected to the exact same Docker network as Traefik (e.g. `traefik-public` as an `external: true` network). Otherwise, Traefik cannot resolve the container names or route packets to them, resulting in a **502 Bad Gateway**.
  - **Fix**: Add the external network (e.g., `traefik-public`) to both the services and the bottom `networks` definition in your target project's `docker-compose.yml`.
- **Service Networking vs Proxy Placement**: When using Traefik to proxy traffic to applications, the Traefik rule definitions must point to the container/app where the traffic is truly hosted. If a backend API and an Nginx static landing page are split across separate Docker Compose projects/networks, applying `rule=Host('example.com')` to *both* causes Traefik to route all traffic to one (often the landing page), resulting in 404s when navigating to backend routes like `/api` or `/terms`.
  - **Fix 1 (Exclude paths from landing page)**: Apply explicit `!PathPrefix` exclusions in the landing page rule to route specific paths exclusively to the backend. Example: `rule=Host('example.com') && !PathPrefix('/terms', '/privacy', '/api', '/liff', '/_next')`.
  - **Fix 2 (Explicit path inclusions on backend)**: Configure the backend router with explicit `PathPrefix` inclusions and a higher `priority` to intercept those routes before the landing page catch-all.
  - **Fix 3 (Consolidate into single Next.js app - Recommended)**: Move the static HTML into Next.js's `public/` directory (e.g. `public/index.html`) and configure a Next.js rewrite rule to map `/` to `/index.html`. Serve both from a single container, bypassing Traefik routing complexity entirely.
- **Frontend App Becomes Silent 404 Catch-All**: When file-provider/app routers overlap, the frontend router can accidentally consume every host path—including API routes—returning HTML 404 instead of backend JSON. Detect this when `curl /api/...` returns `<!DOCTYPE html>` with a Next.js 404 page.
  - Root cause: app router rule is too broad or API routes are not excluded from the frontend router.
  - Fix: explicitly exclude API paths from the frontend rule; verify with backend router rules and `curl -I` on `/api/...` after every change.
- Router without entryPoint — defaults may not be what you expect
- Staging server: use `caServer: https://acme-staging-v02.api.letsencrypt.org/directory` until working to avoid rate limits
- ACME storage not persisted — certificates regenerated, hits rate limit
- Dashboard exposed without auth — `api.insecure=true` is dangerous in production
- PathPrefix without StripPrefix — backend receives full path, may 404
- Services on different ports — each needs explicit port label
- **Name.com DNS Challenge `Permission Denied`**: Check for trailing newlines in `.env` API tokens. Lego fails silently if the token has a `\n` (common when using `echo` or heredocs). Use `echo -n` to create the env file.
- **Name.com `NAMECOM_SERVER` bug**: Setting `NAMECOM_SERVER=https://api.name.com` causes lego to call `https://https//api.name.com`. Leave it unset for production, or use `api.name.com` without the `https://` scheme.
- **TLS certresolver configuration**: Let's Encrypt / ACME certresolver names in Traefik labels must match the exact resolver name defined in Traefik's static configuration. e.g., if Traefik defines `--certificatesresolvers.leresolver.acme.tlschallenge=true`, containers must use `traefik.http.routers.<name>.tls.certresolver=leresolver`, not a default like `myresolver`.
- **Entrypoint names**: Traefik labels routing to an HTTPS entrypoint must use the exact name of the secure entrypoint defined in Traefik's static configuration. Often this is `websecure`, but sometimes it is custom (e.g. `traefik-publicsecure` or `https`).
- **Docker Engine 29.4+ API mismatch**: Traefik v3 hardcodes `GET /v1.24/version` during API negotiation, but Docker >= 29.4.1 requires MinAPIVersion 1.40, causing `client version 1.24 is too old` and failing to discover containers. Workaround: run a TCP relay that rewrites `/v1.24/` to `/v1.40/` in all HTTP requests on the stream (see `traefik-docker29-fix`).

## File Provider
- `watch=true` for hot reload — otherwise restart Traefik on changes
- Can coexist with Docker provider — useful for external services
- Define routers, services, middlewares in YAML — same concepts as labels
- **Docker Mount Links & Dynamic Directory:** Mounting individual files (e.g. `./dynamic.yml:/etc/traefik/dynamic.yml`) inside a container can break file system link notifications (`fsnotify`) on edits from some hosts/editors. **Best practice:** Mount the parent directory (e.g. `./config/dynamic:/etc/traefik/dynamic`) and point the File provider to `directory: /etc/traefik/dynamic` instead of a single `filename`.
- **Docker Internal Routing to Host Services:** To proxy requests from Traefik to a service running on the host system, use `host.docker.internal` (if configured in `extra_hosts` as `host-gateway`). If `host.docker.internal` fails or is refused, target the explicit docker gateway IP of the Traefik container's network (e.g. `http://10.0.2.1:9119` for a container on subnet `10.0.2.0/24`) in the balancer service configuration.
- **Co-hosted Next.js + Backend sanity checks:** see `references/site-routing-fixes.md` for Frontend API route pitfalls, and `references/nextjs-traefik-runtime-checks.md` for rebuild and verification checklist.

## Debugging
- `--log.level=DEBUG` for troubleshooting — verbose but helpful
- Dashboard shows routers, services, middlewares — verify configuration
- `--api.insecure=true` for local dev only — secure with auth in production
