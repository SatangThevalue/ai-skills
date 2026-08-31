---
name: satang-project-suite
description: Develop and deploy Thanapol's custom AI and trading projects.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Next.js
      - FastAPI
      - Trading
      - Computer-Vision
      - Voice-Cloning
---

# Thanapol's Project Suite Development Guide

This guide provides procedures for developing, deploying, and maintaining the portfolio projects of Thanapol Nanthakaset (Satang), covering soundbridgehub, automated trading systems, YOLO flower detection, and voice cloning.

## When to Use
- When writing code or configuring infrastructure for the `soundbridgehub` MP3 e-commerce platform.
- When developing automated trading bots for Forex (XAUUSD), Crypto (BTC), or Stocks using SETTRADE API.
- When implementing YOLO models for flower detection or configuring Voice Cloning/TTS services.

## Prerequisites
- Validate and check user parameters with Pydantic validation (always leverage `Annotated` in dependencies and path operations).
- Implement global error responses as detailed in the template `templates/global_exceptions.py`.

## How to Run
- Execute testing, compilation, and deployment commands using the `terminal` tool.
- Apply database migrations and code changes using `patch` or `write_file` tools.

## Quick Reference
- Run next.js dev: `pnpm dev`
- Run FastAPI server: `uvicorn main:app --reload`
- Trigger Prefect workflow: `prefect flow-run execute`

## Procedure

### 1. SatangTheBank (Next.js + FastAPI + Better-Auth + Beam)
1. **Security & Compliance:** 
   - All LINE webhooks must check `AppUser.consent_finance_data` in `app/api/routers/webhooks.py` before AI processing.
   - Admin routes in FastAPI require `get_current_admin` dependency which validates sessions against `better-auth` (`auth_user`, `auth_session` tables).
2. **Refund Automation:**
   - Use `app/api/routers/membership.py` endpoints for refund requests.
   - Admin-approved refunds trigger `BeamPaymentService.refund_payment()`.
3. **Admin Dashboard:**
   - Monitor pending refunds at `GET /membership/refunds/pending`.
   - Approve refunds via `POST /membership/admin/approve-refund/{order_id}`.
4. **Shared Admin API Layer:** 
   - In Next.js admin pages, export one `lib/admin/api.ts` (`apiGet`, `apiPut`) that reads `NEXT_PUBLIC_ADMIN_KEY` and `NEXT_PUBLIC_API_URL`. Update page components to import it instead of hardcoding headers and URLs inline.
5. **Git & GitHub Workflows for Project Closure:**
   - **Secret Sanitization:** Before pushing changes to public GitHub repositories, run a security check. Ensure environment variable fallbacks in code (like `ADMIN_KEY = os.getenv("ADMIN_KEY")`) do not fall back to hardcoded production secrets.
   - **Strict .gitignore:** Ensure `.env`, `*.pem`, `*.key`, `bot_state_*.json`, and credential files are listed explicitly in `.gitignore` to prevent leakages.
   - **Verification:** Run `git status` and `git diff` before performing any git pushes to verify no sensitive variables or temporary configuration files are staged.
6. **Global Exception & Error Handling:**
   - Implement a unified global exception handler middleware or exception handlers in `app/core/exceptions.py`.
   - Ensure all responses follow a standard format for errors: `{"success": false, "error": {"code": error_code, "message": message, "details": details_or_validation_errors}}`.
   - Catch FastAPI `RequestValidationError` to return readable Pydantic validation details (field path, error type, and message) under the unified JSON error format.
   - Catch `SQLAlchemyError` / `SQLModelError` globally to log the raw queries and stack traces on the server side (via `structlog`) but reply with a sanitized message to prevent database schema exposure.
   - Map custom exceptions inheriting from a project-wide `AppBaseException` to handle business rule errors (e.g. insufficient funds, quota exceeded) cleanly.
### 5. Webhook Development Pitfalls:

   ## Webhook Implementation Pitfalls
   - **401 Unauthorized during Verify:** Often caused by signature mismatch. Use `line-bot-sdk` (v3) `WebhookHandler` for guaranteed compliance. Ensure `LINE_CHANNEL_SECRET` in `.env` is exact, with no whitespace.
   - **Raw Body Requirement:** LINE signature verification MUST be done on the raw request body (bytes). If using FastAPI, do `body = await request.body()` and use `handler.handle(body.decode('utf-8'), signature)`.
   - **Async/Sync:** FastAPI is async, ensure `WebhookHandler` is used in a way that respects the event loop.
   - **SSL/DNS Challenge:** When using Traefik, ensure `certResolver` properly set.
   - **Port Allocation Mismatch:** When deploying multiple docker services, database containers may map to custom external ports (e.g. `5433->5432`) to avoid conflicts with other system postgres instances. Always check `docker ps` to verify the actual external port before setting connection URLs for host-native services.
   - **JSON Interpolation Syntax:** When using raw requests for LLM extraction or completions, avoid formatting raw JSON strings in python f-strings directly using single braces `{}` (e.g. `f"Return JSON: {'amount': 0}"`), as Python interprets it as a format specifier and throws a `ValueError`. Use doubled braces `{{}}` or fallback to normal string concatenation.
   - **Docker Hostname Mismatch:** Native host processes cannot resolve internal Docker Compose container names (like `satangthebank-db`). If the database runs in a container but the backend API runs natively on the host (often to save memory/resource constraints), the connection string must point to `localhost:<host_mapped_port>` instead of `<container_name>:5432`.
   - **SSL Requirements:** Webhooks require valid SSL/TLS from a public CA (e.g., Let's Encrypt). Self-signed certificates trigger SSL errors.
   - **Routing:** For combined Next.js + FastAPI deployments, use Traefik `PathPrefix` rules in `dynamic` config to route `/webhook` and `/api` to the Backend API container and default to Next.js. Remember that when configuring Traefik in `docker-compose.yml`, you must explicitly specify the correct external network name (e.g. `traefik-public`) rather than defaulting to `web`, and ensure entrypoints (like `traefik-publicsecure`) and resolvers (like `leresolver`) match the specific host configuration.
   - **AI Token Management:** Use `llm_service.py` to interface with `cli-proxy-api`. Always use `response_format={"type": "json_object"}` for structured extraction.

### 4. Soundbridgehub Development (Next.js + better-auth + PostgreSQL)
1. Initialize/navigate to the Next.js e-commerce repository.
2. Verify the PostgreSQL connection and run Better-Auth migration:
   ```bash
   pnpx better-auth generate
   ```
3. Set up the local environment variables for JWT and authentication in `.env.local`:
   ```env
   BETTER_AUTH_SECRET=your_jwt_secret_here
   BETTER_AUTH_URL=http://localhost:3000
   DATABASE_URL=postgresql://user:pass@localhost:5432/soundbridgehub
   ```

### 2. Automated Trading Systems (SETTRADE + Python + MQL5)
1. Set up a secure Python environment using `uv` to handle market execution scripts.
2. Integrate SETTRADE API for Thai stocks or MQL5 script loops for XAUUSD/BTC.
3. Schedule ingestion and execution pipelines using Prefect:
   ```python
   # pipeline.py
   from prefect import flow
   @flow
   def execute_trading_strategy():
       # Fetch data & place order logic
       pass
   ```

### 3. YOLO Flower Detection & CV (FastAPI + YOLO)
1. Install OpenCV and Ultralytics under `uv`:
   ```bash
   uv pip install ultralytics opencv-python fastapi uvicorn
   ```
2. Build a FastAPI endpoint to receive image uploads and run inference:
   ```python
   # main.py
   from fastapi import FastAPI, UploadFile
   from ultralytics import YOLO
   app = FastAPI()
   model = YOLO("yolov8n.pt") # Edible flower model
   @app.post("/predict")
   async def predict(file: UploadFile):
       # Run inference and return classes
       pass
   ```

## Pitfalls
- **MQL5 execution**: MQL5 requires a Windows/Wine environment to run MetaEditor/Terminal. Ensure scripts bridge data correctly via socket/REST to the Python controller if running on Linux.
- **Better-Auth Cookie domain**: Ensure `BETTER_AUTH_URL` matches host headers to avoid session dropouts.
- **Docker gateway IP for host services**: When backend runs inside Docker and must call a host-bound proxy such as `cli-proxy-api` on port 42869, cannot use `localhost` from inside a container. Inspect network gateway with `docker network inspect <project>_default | grep Gateway`, then use that gateway IP in client configs.
- **Non-reloaded Docker edits**: Editing `.env`, `admin_routes.py`, or `ai_parser.py` on the host does not update running containers. Always `docker compose up -d --build <service>` after source/env changes.
- **Database Ransomware Recovery**: If the database container logs show repeated `FATAL: role "postgres" is not permitted to log in` and the data volume only contains a database named `readme_to_recover`, the database was exposed and hit by a ransomware bot that dropped the data. Recreating the volume or manually recreating the database (`CREATE DATABASE`) and roles (`CREATE USER`), followed by running schema migration (e.g., `SQLModel.metadata.create_all(engine)`), will restore functionality but original data is lost unless restored from backups. Secure exposed ports (e.g., do not map 5433 to 0.0.0.0).
- **Database Container Secrets Sync**: If the backend API container reports `FATAL: role "postgres" is not permitted to log in`, the DB password configured in `docker-compose.prod.yml` (e.g. `POSTGRES_PASSWORD: ...`) likely mismatches what the API container is sending (e.g. `DATABASE_URL=postgresql://...`). Ensure both variables use the exact same password and restart both containers. If permissions are entirely mangled, check `pg_hba.conf` in `/var/lib/postgresql/data` inside the container or clear the volume via `docker compose down -v` (data loss!). If the `postgres` role has explicitly been set to `NOLOGIN` (perhaps for security), and background scripts/cronjobs need to run, you can temporarily enable login via a superuser: `docker exec -i satangthebank-db psql -U <superuser> -d <db> -c "ALTER ROLE postgres WITH LOGIN;"`. Alternatively, configure cronjobs to use the application user role instead of `postgres`.
- **API Server Startup Failures due to Missing Foreign Tables:** If the FastAPI backend crashes on startup with `sqlalchemy.exc.NoReferencedTableError` when trying to run `SQLModel.metadata.create_all(engine)`, it is usually because a SQLModel references a table (like `user.id` or `session.id`) managed by an external system (like Better-Auth). To fix this, change the `foreign_key` reference into a standard `index=True` soft-link in the SQLModel so the backend stops trying to validate foreign tables it doesn't own.
- **Admin key hygiene**: Do not hardcode admin keys in page modules or fallback values. Centralize calls in one `lib/admin/api.ts`, keep header names stable, and inject secret via `NEXT_PUBLIC_ADMIN_KEY` / `ADMIN_KEY`.
- **Git Push Verification**: Before pushing code for project closure, always ensure a strict `.gitignore` is active and that no real secret credentials, dynamic local configurations, or tracking database instances have leaked into git staging. Verify with `git status` and `git diff` first.
- **Next.js admin pages**: Avoid redeclaring `use client`, duplicate imports, or duplicate constants in `page.tsx`. Keep one constant block and one default export.

## Verification
Verify database connectivity and check the API server status:
```bash
curl -I http://localhost:8000/health
```
