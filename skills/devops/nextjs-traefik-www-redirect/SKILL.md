---
name: nextjs-traefik-www-redirect
description: Deploy Next.js standalone app with Traefik www redirection.
version: 0.1.0
metadata:
  hermes:
    tags: [Next.js, Traefik, Docker, Redirect, Deployment]
---

# Next.js Traefik Deployment with WWW Redirect

Deploys a Dockerized Next.js standalone application behind a Traefik reverse proxy. It automatically sets up apex-to-www HTTP redirection (e.g., `domain.com` -> `www.domain.com`) and routes HTTPS traffic using an existing Traefik certificate resolver. 

## When to Use
- The user asks to deploy a web portfolio, Next.js app, or React site.
- You need to configure apex-to-www domain redirection via Traefik labels.
- The project uses Next.js standalone output mode inside Docker.

## Prerequisites
- A Git repository containing a Next.js app and a Dockerfile configured for standalone output.
- A running Traefik instance connected to a known external network (e.g., `traefik-public`).
- A configured Traefik certificate resolver (e.g., `namecom`, `letsencrypt`).

## How to Run
Invoke through the `terminal` tool to clone the repository, `patch` to inject the Traefik routing labels into `docker-compose.yml`, and `terminal` to build and deploy.

## Quick Reference
- Next.js config check: `grep "standalone" next.config.ts`
- Regex for redirect: `^https://example.com/(.*)` -> `https://www.example.com/$${1}`

## Procedure

1. **Clone the Repository**
   Invoke through the `terminal` tool:
   ```bash
   git clone <REPO_URL> /path/to/target && cd /path/to/target
   ```

2. **Verify Dockerfile and Next.js Configuration**
   - Ensure the Dockerfile is properly capitalized. If it is named `dockerfile` (lowercase), rename it: `mv dockerfile Dockerfile`.
   - Use `search_files` or `terminal` to ensure `output: "standalone"` is present in `next.config.ts` or `next.config.js`.

3. **Configure Traefik Labels in Compose**
   Use the `patch` tool to update the `docker-compose.yml`. Add the external network and the Traefik routing labels. Replace `example.com` and `my-resolver` with actual values:
   ```yaml
   services:
     web:
       # ... existing build/env config ...
       networks:
         - traefik-public
       labels:
         - "traefik.enable=true"
         # Route for www.example.com
         - "traefik.http.routers.app-www.rule=Host(`www.example.com`)"
         - "traefik.http.routers.app-www.entrypoints=websecure"
         - "traefik.http.routers.app-www.tls=true"
         - "traefik.http.routers.app-www.tls.certresolver=my-resolver"
         - "traefik.http.services.app-www.loadbalancer.server.port=3000"
         
         # Route for example.com (apex) redirecting to www
         - "traefik.http.routers.app-apex.rule=Host(`example.com`)"
         - "traefik.http.routers.app-apex.entrypoints=websecure"
         - "traefik.http.routers.app-apex.tls=true"
         - "traefik.http.routers.app-apex.tls.certresolver=my-resolver"
         - "traefik.http.routers.app-apex.middlewares=redirect-to-www"
         
         # Middleware for Redirect
         - "traefik.http.middlewares.redirect-to-www.redirectregex.regex=^https://example.com/(.*)"
         - "traefik.http.middlewares.redirect-to-www.redirectregex.replacement=https://www.example.com/$${1}"

   networks:
     traefik-public:
       external: true
   ```

4. **Build and Deploy**
   Invoke through the `terminal` tool (use background mode for Next.js builds as they often exceed 60 seconds):
   ```bash
   docker compose up -d --build
   ```

## Updating an Existing Deployment
When updating the code from Git:
1. **Backup Configs**: `cp docker-compose.yml /tmp/docker-compose-backup.yml` (preserves Traefik labels).
2. **Sync Code**: `git fetch --all && git reset --hard origin/main` to forcefully override local changes (like Dockerfile case renames) and avoid merge conflicts.
3. **Restore Configs**: `cp /tmp/docker-compose-backup.yml docker-compose.yml`
4. **Rebuild**: `docker compose up -d --build` (add `--no-cache` if the site doesn't reflect new changes).

## Pitfalls
- **`npm ci` vs `npm install` inside Docker:** If the `package-lock.json` generated on the host is out of sync with `package.json` (often due to missing or mismatched dependencies), `npm ci` inside the Dockerfile will crash. If this happens, replace `npm ci` with `npm install` in the Dockerfile before building.
- **Lowercase `dockerfile` Git Issues:** If the repository originally committed `dockerfile` with a lowercase `d`, running `mv dockerfile Dockerfile` locally works once. However, subsequent `git pull` operations will likely restore the lowercase `dockerfile` and overwrite or conflict with your changes. To permanently fix this, either rename it via git (`git mv dockerfile Dockerfile; git commit`) or chain the rename during deployment (`git pull && mv dockerfile Dockerfile 2>/dev/null || true && docker compose up -d --build`).
- **Missing Standalone Output:** If `output: 'standalone'` is missing from `next.config.ts`, the Docker build will fail during the `COPY --from=builder /app/.next/standalone ./` step because the directory won't exist.
- **Build Timeouts:** Next.js `npm run build` downloads dependencies and compiles static pages, easily taking 2-3 minutes. Run this in the background with `notify_on_complete=true` to avoid terminal timeouts.

## Verification
Use the `terminal` tool to verify the redirect and the app status:
```bash
curl -sk -I https://example.com
```
Expect an HTTP `302` or `307` pointing to `Location: https://www.example.com/`.