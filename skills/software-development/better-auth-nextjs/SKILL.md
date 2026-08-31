---
name: better-auth-nextjs
description: Configure modern authentication in Next.js using better-auth.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Next.js
      - Authentication
      - Better-Auth
      - JWT
---

# Authentication in Next.js with Better-Auth

Implement type-safe, developer-friendly authentication using `better-auth` in Next.js applications, utilizing JWTs or session cookies.

## When to Use
- When adding auth features (sign up, sign in, OAuth, sessions) to a Next.js App Router project.
- When configuring database adapters for PostgreSQL with auth tables.

## Prerequisites
- A Next.js project initialized.
- A running PostgreSQL instance or setup.
- `pnpm` installed.

## How to Run
- Manage dependencies, run database migrations, and start development servers using the `terminal` tool.
- Edit client/server config code using the `patch` or `write_file` tools.

## Quick Reference
- **Vanilla PostgreSQL Schema**: See `references/postgres-vanilla-schema.sql` for manual setup without an ORM.
- Install library: `pnpm add better-auth`
- Run DB migration: `pnpx better-auth generate`

## Procedure

1. **Install Better-Auth**
   Install the main package in your Next.js project:
   ```bash
   pnpm add better-auth
   ```

2. **Configure the Auth Server**
   Create a configuration file at `lib/auth.ts`:
   ```typescript
   import { betterAuth } from "better-auth";
   import { pgAdapter } from "better-auth/adapters"; // or prisma/drizzle
   
   export const auth = betterAuth({
       database: {
           // Database connection configuration
       },
       emailAndPassword: {
           enabled: true
       }
   });
   ```

3. **Set Up the Next.js API Route**
   Create an API handler at `app/api/auth/[...better-auth]/route.ts`:
   ```typescript
   import { auth } from "@/lib/auth";
   import { toNextJsHandler } from "better-auth/next-js";
   
   export const { POST, GET } = toNextJsHandler(auth);
   ```

4. **Verify Session on Server Side**
   Retrieve the current session in your Next.js Server Components:
   ```typescript
   import { auth } from "@/lib/auth";
   import { headers } from "next/headers";
   
   // inside server component
   const session = await auth.api.getSession({
       headers: await headers()
   });
   ```

```
- **Module not found for `better-auth/next`**: In Better-Auth v1.6.23+, the API export changed. You must import `toNextJsHandler` from `"better-auth/next-js"` and pass `auth` instead of importing `toNextRouteHandler` from `"better-auth/next"`.
- **Database Migrations on Empty Databases**: If your database volume is cleared or re-created, Better-Auth's tables (`user`, `session`, `account`, `verification`) will disappear. The app will fail silently on login/signup or return `relation "user" does not exist`. You MUST re-create the tables (via `npx @better-auth/cli migrate` or raw SQL `CREATE TABLE "user" (...)`). Make sure all camelCase columns (`expiresAt`, `emailVerified`, etc.) are double-quoted in raw SQL.
- **Environment Variables**: Ensure `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL` are defined in your `.env` file. For production, `BETTER_AUTH_SECRET` must be at least 32 characters long or a warning will appear in the Next.js build logs.
- **Better-Auth Integration**: FastAPI reads `session` tokens from the same DB as Next.js; treat these tables as Read-only from the FastAPI side. Ensure SQLModel definitions match the Better-Auth schema exactly (User, Session).
- **PostgreSQL camelCase & Case Sensitivity**: Better-Auth expects camelCase column names (e.g. `emailVerified`, `userId`, `expiresAt`, `createdAt`). In PostgreSQL, column names without double-quotes are automatically normalized to lowercase. To avoid `column account.userId does not exist` errors, always wrap camelCase columns in double-quotes in raw SQL migration scripts (e.g., `CREATE TABLE account ( "userId" TEXT NOT NULL, "expiresAt" TIMESTAMP )`).
- **Password Hash Algorithms**: Better-Auth utilizes specific password hashing (such as scrypt or pbkdf2) internally. Manually hashing passwords using external libraries like `bcrypt` and inserting them directly into the `account` table will result in `Error: Invalid password hash` exceptions. To create users programmatically, always register them through the Better-Auth API layer (e.g. `/api/auth/sign-up/email`) to ensure correct cryptographic hashing.
- **Docker Container Networking**: When running Next.js within a Docker container, using `localhost:5433` (the host-forwarded port) for the Better-Auth database pool connection will result in `ECONNREFUSED` errors. Configure the connection string to use the internal Docker container name and standard port (e.g. `postgresql://postgres:***@satangthebank-db:5432/satangthebank`) for inter-container communication.
- **Traefik Reverse Proxy & Invalid Origin**: Better-Auth employs CSRF checking by comparing incoming requests with the configured `BETTER_AUTH_URL` or Host headers. When behind a reverse proxy (like Traefik) that handles SSL termination and forwards HTTP requests to Next.js on port 3000, Better-Auth might throw an `Invalid origin` error. To resolve this, explicitly configure `trustedOrigins: ["https://your-production-domain.com"]` in the `betterAuth({...})` config options. Also, make sure that `BETTER_AUTH_URL` is set in the runtime container environment (e.g. via `docker-compose.prod.yml`) and not just at build time.
- **Account Linking & Client Limitations**: Better-Auth client-side `authClient.linkAccount({ provider: "credential", ... })` is restricted on OAuth/social accounts due to security controls (e.g. setting passwords cannot be triggered directly from client code). To allow an OAuth user (like LINE OIDC) to bind an email and password for cross-device logins, you must implement a server-side route that wraps the request and calls the secure server API:
  ```typescript
  // apps/frontend/src/app/api/auth/link-credential/route.ts
  import { auth } from "@/lib/auth";
  import { headers } from "next/headers";

  export async function POST(req: Request) {
      const session = await auth.api.getSession({ headers: await headers() });
      if (!session) return Response.json({ success: false }, { status: 401 });
      
      const { email, password } = await req.json();
      // 1. Update user email in DB using SQL / ORM
      // 2. Call secure server-side API to set password:
      await auth.api.setPassword({
          body: { newPassword: password },
          headers: await headers()
        });
      return Response.json({ success: true });
  }
  ```
- **Next.js Static Generation (SSG) & Auth Config Cache**: Next.js builds page routes during compile time. If static pages contain dynamic auth adapters or connection parameters, verify that the environment variables (like `DATABASE_URL`) are populated in your Docker compose configuration or build phase to prevent compile-time connection issues.
- **Database Migrations:** Better-Auth does *not* auto-migrate its schema on start. You must generate and apply migrations, or manually create the required tables (`user`, `session`, `account`, `verification`) in your database.
- **Database Hooks & User Auto-Provisioning:** Better-Auth provides `databaseHooks` for side effects. For example, to automatically provision records when a user registers, hook into `user.create.after`.
  ```typescript
  databaseHooks: {
      user: {
          create: {
              after: async (user) => {
                  // Execute raw queries or ORM inserts here using the new user.id
              }
          }
      }
  }
  ```
- **CORS Issues**: Ensure `BETTER_AUTH_URL` matches the exact URL of your application in development and production. If running behind a reverse proxy (like Traefik), ensure headers like `X-Forwarded-Host` are passed correctly.
- **Environment Variables**: For Next.js client-side requests, remember to prefix API URLs with `NEXT_PUBLIC_` (e.g., `NEXT_PUBLIC_API_URL`). If FastAPI acts as a gateway on a separate domain (e.g., `api.example.com`), configure FastAPI's CORSMiddleware with `allow_origins=["https://app.example.com"]` and `allow_credentials=True`.
- **Organization & Role Management**: Better-Auth requires proper database initialization for its plugins. If you are using the `organization` plugin for multi-tenant setups, ensure your database schema (User, Organization, Member) strictly matches the Better-Auth expected schema, and that you initialize the DB adapter correctly before attempting to create roles.

## Verification
Confirm the API routes are listening:
```bash
curl -I http://localhost:3000/api/auth/session
```
