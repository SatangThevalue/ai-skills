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
   import { toNextRouteHandler } from "better-auth/next";
   
   export const { POST, GET } = toNextRouteHandler(auth);
   ```

4. **Verify Session on Server Side**
   Retrieve the current session in your Next.js Server Components:
   ```typescript
   import { auth } from "@/lib/auth";
   import { headers } from "next/headers";
   
   const session = await auth.api.getSession({
       headers: await headers()
   });
   ```

## Pitfalls
- **Environment Variables**: Ensure `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL` are defined in your `.env` file.
- **CORS Issues**: Ensure `BETTER_AUTH_URL` matches the exact URL of your application in development and production.

## Verification
Confirm the API routes are listening:
```bash
curl -I http://localhost:3000/api/auth/session
```
