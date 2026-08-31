# Docker Compose Production Checklist

When migrating a monorepo Next.js + FastAPI stack to Docker Compose:

1. **Host Native Fallback**: On small VPS environments (e.g. 4GB RAM), `next build` inside a container can trigger OOM kills, leading to 502 Bad Gateway via Traefik. A hybrid "Host Native" approach (DB in Docker, Next.js and FastAPI run natively via PM2) provides better stability.

2. **Next.js Dockerfile in pnpm Workspaces**:
   - `pnpm install` in CI/Docker often halts on `node_modules` purges. Set `ENV CI=true` and `RUN pnpm config set confirmModulesPurge false` before installation.
   - Run `pnpm install --frozen-lockfile=false --ignore-workspace` within the specific app directory if you encounter workspace resolution issues.
   - CRITICAL: In the runner stage, you must copy the root `node_modules` in addition to the app-level `node_modules` because pnpm symlinks workspace dependencies.
     ```dockerfile
     COPY --from=builder /app/node_modules /app/node_modules
     COPY --from=builder /app/apps/frontend/node_modules ./node_modules
     ```

3. **Database Connection Strings**:
   - Inside docker-compose, FastAPI must connect to the DB container by its service name (`postgresql://postgres:password@satangthebank-db:5432/db`), not `localhost`.
   - Never use placeholder asterisks (`***`) or sed-based replacements for passwords in automated scripts, as partial sed failures leave the `***` intact, resulting in `FATAL: password authentication failed`. Use Environment Variables or hardcode via a direct `cat` overwrite during the setup phase.

4. **Database Table Creation**:
   - `SQLModel.metadata.create_all(engine)` may fail to create tables if executed during the `startup` event before the DB container is fully ready.
   - Always run an explicit manual migration (or script) during deployment:
     ```bash
     docker exec db-container psql -U postgres -d dbname -c "CREATE TABLE IF NOT EXISTS ..."
     ```