# Next.js 14 App Router Admin Best Practices

## 1. The `layout.tsx` Export Trap
**Problem:** Next.js App Router strictly enforces what can be exported from `layout.tsx` and `page.tsx` files. If you export a utility function (like a fetch wrapper or constants) from a layout file, the build will fail with `Type error: Layout does not match the required types of a Next.js Layout. "xyz" is not a valid Layout export field.`
**Solution:** Move all non-component, non-metadata exports to a dedicated `src/lib/` or `src/utils/` directory.

## 2. The 404 Cache Trap & Docker Build Cache
**Problem:** If a Next.js build fails on a specific route (e.g., `/admin`), the dev server or build process might cache the 404 state. Even after fixing the underlying code error, navigating to that route will inexplicably return a 404. Furthermore, running `docker compose up -d --force-recreate` on a Next.js container does not refresh files or rebuild client-side cache built into the image layers.
**Solution:** Stop the server, delete the `.next` directory (`rm -rf .next`), and rebuild cleanly (`pnpm build`). In Docker environments, trigger a complete cache-free rebuild of the image:
```bash
docker compose -f docker-compose.prod.yml build --no-cache satangthebank-web
docker compose -f docker-compose.prod.yml up -d satangthebank-web
```

## 3. Better-Auth ECONNREFUSED inside Docker Containers
**Problem:** A Next.js frontend running inside a Docker container (`satangthebank-web`) cannot access the database using `localhost:5433` (the host-mapped port) or `127.0.0.1:5433` because localhost inside a container refers to the container itself. Attempting to sign in or call auth APIs will return a HTTP 500 error, and container logs will show connection refusal errors.
**Solution:** Configure the database connection string in `src/lib/auth.ts` to use the database service container name directly on the shared Docker Network (e.g., `satangthebank-db:5432`) instead of localhost or host IP gateway. Also, declare `DATABASE_URL` in the environment block of your Next.js service in `docker-compose.yml` to supply runtime values.

## 4. Docker Volume Database Password Desync
**Problem:** When changing the `POSTGRES_PASSWORD` environment variable in `docker-compose.yml`, a pre-existing Docker Volume (e.g., `satangthebank_pgdata`) will retain its original password configuration (e.g., `satangthevalue`), leading to `password authentication failed for user "postgres"` (FATAL 28P01) errors on newly built containers using the new password.
**Solution:** Either adjust the connection string to use the volume's original password, or perform a clean recreate of the database environment by dropping the volume:
```bash
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up -d
```

## 5. Server vs Client Components
When building simple static dashboards or layout wrappers, prefer Server Components (the default). Only add `"use client"` when you need hooks like `useState`, `useEffect`, or `usePathname`. Unnecessary client boundaries can complicate routing and hydration.

## 6. Protected API Routes
When securing an `/api/admin/*` route in FastAPI (the backend), you don't always need a complex JWT setup initially. A simple `x-admin-key` header checked via a FastAPI dependency is sufficient to protect administrative endpoints from public access while allowing the Next.js frontend to fetch data securely.