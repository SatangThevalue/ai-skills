---
name: hybrid-fastapi-line-deployment
description: Deploy and debug FastAPI LINE bots behind Traefik.
version: 0.2.0
metadata:
  hermes:
    tags:
      - FastAPI
      - LINE
      - Traefik
      - Next.js
---

# Hybrid FastAPI and LINE Webhook Deployment

This skill provides a procedure for deploying and debugging a FastAPI backend that handles LINE webhooks, integrates with a local AI proxy, connects to a PostgreSQL container behind a Traefik reverse proxy, and pairs with a Next.js App Router frontend.

## When to Use
- When a FastAPI LINE bot fails to communicate with a PostgreSQL container behind Traefik.
- When LINE Webhooks timeout waiting for slow AI processing (OCR/LLMs).
- When optimizing LINE Messaging costs (Push API vs Reply API).
- When building Next.js App Router frontends and encountering layout/page export type errors.
- When organizing multi-wallet or multi-tenant database isolation in a financial SaaS bot.

## Prerequisites
- Docker and Traefik configured on the target VPS.
- Valid `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET` in `.env`.
- An active LINE Messaging API Channel.
- Local AI proxy or model server running on a specific port (e.g., `42869`).

## How to Run
- Modify routing dynamically in Traefik's configuration file using the `patch` or `write_file` tool.
- Run the FastAPI backend in native host mode by executing `uvicorn` inside the `terminal` tool.

## Procedure

1. **Configure Traefik for Host-Native Services:**
   When running the API natively on the host instead of inside a Docker container, update the dynamic Traefik configuration file. Change the service loadBalancer server URL to point to the host gateway IP (`10.0.0.1` or `10.0.2.1` depending on `docker0` or proxy network gateway) on the service port (e.g., `8000`) instead of the container name.
   ```yaml
   services:
     satangthebank-api-srv:
       loadBalancer:
         servers:
           - url: http://10.0.0.1:8000
   ```

2. **Handle Database Resolution in Hybrid Setup:**
   Ensure the database connection string uses `localhost` and the mapped host port (e.g., `5433` mapping to container port `5432`) since the API is running natively on the host:
   ```python
   DATABASE_URL = "postgresql://postgres:***@localhost:5433/satangthebank"
   ```

3. **Design a Safe AI Parser:**
   Avoid LangChain `PromptTemplate` parsing errors caused by JSON curly braces in prompt templates by utilizing standard string concatenation or double-escaped braces (`{{ }}`), and querying the local server directly via `requests`. Enforce data consistency by providing an exact list of allowed categories in the prompt and writing a fallback (`if result.get("category") not in ALLOWED_CATEGORIES: ...`) in Python.

4. **Optimize LINE Webhooks with BackgroundTasks:**
   To prevent LINE webhook timeouts (HTTP 504) while waiting for slow AI processing (e.g., multiple OCR image requests), use FastAPI `BackgroundTasks`.
   ```python
   from fastapi import FastAPI, Request, BackgroundTasks

   @app.post("/webhooks/line")
   async def line_webhook(request: Request, background_tasks: BackgroundTasks):
       body = await request.body()
       events = json.loads(body.decode("utf-8")).get("events", [])
       if events:
           background_tasks.add_task(process_line_events, events)
       return {"status": "ok"} # Return immediately to ack LINE
   ```

5. **Zero-Cost LINE Replies:**
   Even in background tasks, use `ReplyMessageRequest` instead of `PushMessageRequest` to avoid consuming the 1,000 messages/month free quota. The `replyToken` is valid for 1 minute, which is usually enough for fast LLM processing even for batches of images.

6. **LINE Loading Animation:**
   Improve UX during background AI processing by showing a loading animation (up to 60 seconds):
   ```python
   line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=line_user_id, loadingSeconds=40))
   ```

7. **System Command Bypass:**
   Do not send explicit system commands (e.g., "สรุปยอด") to the LLM. Intercept them early in the webhook handler to save token costs and prevent hallucinations, fetching data directly from the DB and responding immediately.

## Pitfalls
- **Next.js Layout Export Error**: `Type error: Layout "src/app/.../layout.tsx" does not match the required types...` occurs when you export utility functions (e.g., `export function adminFetch()`) from a Next.js App Router file. `layout.tsx` and `page.tsx` must ONLY export the component and metadata. Move utilities to a separate `src/lib/` file. See `references/nextjs-admin-dashboard.md`.
- **Next.js 404 Cache Trap**: If a Next.js App Router page fails to build due to an error, Next.js may cache the 404 state. Even after fixing the code, the page might still return 404. Run `rm -rf .next` before rebuilding to clear the stale cache. See `references/nextjs-admin-dashboard.md`.
- **Better-Auth ECONNREFUSED in Docker Container**: Next.js frontends running inside a Docker container (`satangthebank-web`) cannot access the database using `localhost:5433` (the mapped host port). Instead, configure the DB connection string to use the container name directly (`satangthebank-db:5432`) on the shared Docker Network to resolve connectivity errors. Ensure `DATABASE_URL` is explicitly defined in `docker-compose.yml` for runtime access in production containers.
- **Better-Auth Database Casing Handshake (PostgreSQL)**: Better-Auth queries the PostgreSQL database using explicit camelCase quotes (e.g. `"userId"`, `"expiresAt"`). If the DB schema was generated as lowercase/snake_case (`userid` or `user_id` without quotes), Better-Auth will throw errors like `column account.userId does not exist`. Table recreation must use double quotes around column names to enforce case preservation.
- **Better-Auth CSRF Invalid Origin**: Better-Auth blocks authentication requests if the requested Origin doesn't match the `BETTER_AUTH_URL` environment variable. When running behind Traefik (where SSL termination occurs at the proxy and requests enter Next.js via HTTP), Better-Auth may detect host-origin mismatch and throw `Invalid origin`. Resolve this by setting `trustedOrigins: ["https://yourdomain.com"]` in `src/lib/auth.ts` and ensuring `BETTER_AUTH_URL` is correctly set to the public HTTPS URL in the docker-compose environment variables (NOT compiled hardcoded in .env.local if .env.local is in .gitignore).
- **Better-Auth Password Encryption Hash Mismatch**: Do not attempt to manually hash passwords using host utilities (e.g., standard Python bcrypt) and insert them into the `account` table directly, as Better-Auth uses standard PBKDF2/scrypt key derivation internally. Standard bcrypt hashes will yield `Invalid password hash` errors. Create test credentials by calling the Better-Auth `/api/auth/sign-up/email` REST endpoint directly via `requests` or `curl`, allowing the framework's adapter to correctly hash and persist the password.
- **Traefik Route Hijacking Next.js API Routes**: If Traefik is configured to route all `/api` traffic to a backend container/port (e.g., `(PathPrefix(\`/api\`) || PathPrefix(\`/webhooks\`))`), it will accidentally hijack Next.js API routes (like `/api/auth/*` for Better-Auth). To resolve this routing conflict, explicitly negate Next.js paths in Traefik's rule block: `(PathPrefix(\`/api\`) && !PathPrefix(\`/api/auth\`))`.
- **Docker Compose Cache Recreate Failure**: Running `docker compose up -d --force-recreate` on a Next.js container does not refresh files or rebuild client-side cache built into the image layers. Use `docker compose build --no-cache <service>` followed by `docker compose up -d <service>` when connection configs or static pages are updated.
- **Traefik 502 Bad Gateway**: Forwarding to `localhost:8000` resolves inside Traefik's container. Use the host gateway IP (e.g., `10.0.0.1`).
- **F-String Template Collision**: Literal JSON `{ "key": "value" }` inside Python f-strings causes `ValueError: Invalid format specifier`. Use plain string concatenation or double braces `{{ }}`.
- **LINE Invalid Reply Token**: Getting an `Invalid reply token` (HTTP 400) during local curl testing is expected when using a dummy token, but it proves the payload successfully reached LINE's servers.
- **Background Port Lockout**: If `uvicorn` crashes or is killed but leaves a locked port, use `fuser -k 8000/tcp` to release it.
- **Background Task `UnboundLocalError`**: When sharing variables (like `text`) across conditional blocks (e.g., `msg_type == "text"` vs `"image"`), ensure variables are initialized with empty/default values outside the condition before passing them to parsers or telemetry logs.